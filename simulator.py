import numpy as np
from Config import *
from policies import get_policy_functions

def count_busy_servers(server_state):
    busy_servers = sum(1 for state in server_state if state == "BUSY")
    return busy_servers

def calculate_current_power(server_state):
    current_power = 0
    for state in server_state:
        if state == "BUSY":
            current_power += P_BUSY
        elif state == "IDLE":
            current_power += P_IDLE
        elif state == "OFF":
            current_power += P_OFF
        elif state == "SETUP":
            current_power += P_SETUP
        else:
            raise ValueError("Unknown state")
    return current_power

def get_arrival_rate(Num_server, base_arrival_rate, arrival_model = "fixed", C = 0.3, alpha = 0.5):
    '''
    arrival_model
    fixed: a fixed arrival rate
    scaling: lambda^n = n - C * n^alpha
    '''
    if arrival_model == "fixed":
        return base_arrival_rate

    elif arrival_model == "scaling":
        arrival_rate = Num_server - C * (Num_server ** alpha)

        if arrival_rate <= 0:
            raise ValueError("Arrival rate must be positive")
        return arrival_rate

    else:
        raise ValueError("Unknown arrival mode")

def start_service(server_id, arrival_time, current_time, service_rate, server_state, current_customer_arrival, event_calendar):

    # Set the server to busy state
    server_state[server_id] = "BUSY"

    current_customer_arrival[server_id] = arrival_time
    departure_time = current_time + np.random.exponential(1 / service_rate)
    event_calendar.append((departure_time, "departure", server_id))

def start_setup(server_id, current_time, setup_time, server_state, event_calendar):

    # Set the server to setup state
    server_state[server_id] = "SETUP"

    setup_complete_time = current_time + setup_time
    event_calendar.append((setup_complete_time, "setup_complete", server_id))

def apply_setup_policy(central_queue, current_time, setup_time,
                       server_state, event_calendar, policy_functions):
    if policy_functions["should_start_setup"](central_queue, server_state):
        off_server = policy_functions["choose_off_server"](server_state)

        if off_server is not None:
            start_setup(
                off_server,
                current_time,
                setup_time,
                server_state,
                event_calendar
            )

def find_idle_server(server_state):
    for i, state in enumerate(server_state):
        if state == "IDLE":
            return i
    return None

def dispatch_jobs_to_idle_servers(central_queue, current_time, service_rate,
                                  server_state, current_customer_arrival,
                                  event_calendar):
    added_waiting_time = 0
    added_started_service = 0

    while len(central_queue) > 0:
        idle_server = find_idle_server(server_state)

        if idle_server is None:
            break

        arrival_time = central_queue.pop(0)

        waiting_time = current_time - arrival_time
        added_waiting_time += waiting_time
        added_started_service += 1

        start_service(idle_server, arrival_time, current_time, service_rate, server_state, current_customer_arrival,
                      event_calendar)

    return added_waiting_time, added_started_service

def server_simulator(Num_server = 5,
                     arrival_rate = 1,
                     service_rate = 1.5,
                     timesteps = 100,
                     setup_time = SETUP_TIME,
                     policy = "NEVEROFF",
                     arrival_model = ARRIVAL_MODEL,
                     arrival_scale_C = ARRIVAL_SCALE_C,
                     arrival_alpha = ARRIVAL_ALPHA,
                     seed = 42):
    '''
    Num_server: The number of server in the system
    arrival_rate: The arrival rate lambda
    service_rate: The service rate mu
    timesteps: Simulation times
    setup_time: The setup time
    return: Average_System_Size L, Utilization rho, Average_Power, Average_Waiting_Time, Average_Response_Time, ERP
    '''

    # Set the random seed
    if seed is not None:
        np.random.seed(seed)

    ## Initialisation

    #get the arrival rate
    actual_arrival_rate = get_arrival_rate(
        Num_server,
        arrival_rate,
        arrival_model,
        arrival_scale_C,
        arrival_alpha
    )
    policy_functions = get_policy_functions(policy)
    server_state = [policy_functions["initial_state"]] * Num_server # B(t): The cpu is in use, or idle

    # Central queue
    central_queue = []

    Area_server_state = 0 # AB
    Area_users = 0  # AQ

    total_energy = 0
    total_waiting_time = 0
    Num_started_service = 0
    total_response_time = 0
    Num_completed_users = 0
    current_customer_arrival = [None] * Num_server

    # Initialise the event calendar
    first_arrival_time = np.random.exponential(1/actual_arrival_rate)
    event_calendar = [(first_arrival_time, "arrival", None), (timesteps, "termination", None)]

    current_time = 0

    while True:
        # Find the next event and delete it from the event calendar
        next_index = min(range(len(event_calendar)), key=lambda i: event_calendar[i][0])
        event_time, event_type, server_id = event_calendar.pop(next_index)

        delta_time = event_time - current_time

        # Update AQ and AB
        busy_server = count_busy_servers(server_state)
        system_size = busy_server + len(central_queue)

        Area_users += delta_time * system_size
        Area_server_state += delta_time * busy_server

        # Update energy consumption
        current_power = calculate_current_power(server_state)

        total_energy += delta_time * current_power

        # Update the current time
        current_time = event_time

        if event_type == "arrival":
            # arrival event
            arrival_time = current_time

            # New jobs enter the central queue
            central_queue.append(arrival_time)

            # Dispatcher jobs to idle server
            added_waiting_time, added_started_service = dispatch_jobs_to_idle_servers(
                central_queue,
                current_time,
                service_rate,
                server_state,
                current_customer_arrival,
                event_calendar)

            total_waiting_time += added_waiting_time
            Num_started_service += added_started_service

            apply_setup_policy(central_queue,
                               current_time,
                               setup_time,
                               server_state,
                               event_calendar,
                               policy_functions)

            # Schedule the next arrival time
            next_arrival_time = current_time + np.random.exponential(1 / actual_arrival_rate)
            event_calendar.append((next_arrival_time, "arrival", None))

        elif event_type == "departure":

            response_time = current_time - current_customer_arrival[server_id]
            total_response_time += response_time
            Num_completed_users += 1
            current_customer_arrival[server_id] = None

            # Server becomes idle after completing a job
            server_state[server_id] = "IDLE"

            # Dispatch another job to the idle server
            added_waiting_time, added_started_service = dispatch_jobs_to_idle_servers(
                central_queue,
                current_time,
                service_rate,
                server_state,
                current_customer_arrival,
                event_calendar
            )

            total_waiting_time += added_waiting_time
            Num_started_service += added_started_service

            # If the server is still idle after dispatching, apply policy
            if server_state[server_id] == "IDLE":
                server_state[server_id] = policy_functions["idle_state_after_departure"]

        elif event_type == "setup_complete":
            # Server becomes idle after completing a job
            server_state[server_id] = "IDLE"

            # Dispatch another job to the idle server
            added_waiting_time, added_started_service = dispatch_jobs_to_idle_servers(
                central_queue,
                current_time,
                service_rate,
                server_state,
                current_customer_arrival,
                event_calendar
            )

            total_waiting_time += added_waiting_time
            Num_started_service += added_started_service

            # If the server is still idle after dispatching, apply policy
            if server_state[server_id] == "IDLE":
                server_state[server_id] = policy_functions["idle_state_after_departure"]

        elif event_type == "termination":
            Average_System_Size = Area_users/timesteps # L
            Utilization = Area_server_state / (Num_server * timesteps) # rho

            Average_Power = total_energy / timesteps
            if Num_started_service > 0:
                Average_Waiting_Time = total_waiting_time / Num_started_service
            else:
                Average_Waiting_Time = 0
            if Num_completed_users > 0:
                Average_Response_Time = total_response_time / Num_completed_users
            else:
                Average_Response_Time = 0

            ERP = Average_Power * Average_Response_Time

            return Average_System_Size, Utilization, Average_Power, Average_Waiting_Time, Average_Response_Time, ERP

if __name__ == "__main__":
    Average_System_Size, Utilization, Average_Power, Average_Waiting_Time, Average_Response_Time, ERP = server_simulator(
        Num_server=5,
        arrival_rate=1,
        service_rate=1.5,
        timesteps=100,
        policy="NEVEROFF",  # "INSTANTOFF", "NEVEROFF"
        arrival_model="scaling",
        arrival_scale_C=0.3,
        arrival_alpha=0.5,
        seed=42)

    print("Simulation Finished")
    print("The Average System Size:", Average_System_Size)
    print("Utilization:", Utilization)
    print("Average Power:", Average_Power)
    print("Average Waiting Time:", Average_Waiting_Time)
    print("Average Response Time:", Average_Response_Time)
    print("ERP:", ERP)