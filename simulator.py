import numpy as np
from Config import *

def choose_server(Num_users, policy):
    '''
    Choose the server based on the policy
    '''
    if policy == "NEVEROFF":
        return np.argmin(Num_users)
    else:
        raise ValueError("Unknow policy")

def count_busy_servers(atm_state):
    '''
    Count the number of busy servers
    '''
    busy_servers = sum(1 for state in atm_state if state == "BUSY")
    return busy_servers

def calculate_current_power(atm_state):
    '''
    Calculate the current power
    '''
    current_power = 0
    for state in atm_state:
        if state == "BUSY":
            current_power += P_BUSY
        elif state == "IDLE":
            current_power += P_IDLE
        else:
            raise ValueError("Unknow state")

def multi_ATM_simulator(Num_atm = 5, arrival_rate = 1, service_rate = 1.5, timesteps = 100, policy = "NEVEROFF", seed = 42):
    '''
    Num_atm: The number of ATM in the system
    arrival_rate: The arrival rate lambda
    service_rate: The service rate mu
    return: Average_System_Size L, Utilization rho, Average_Power, Average_Waiting_Time, Average_Response_Time, ERP
    '''

    # Set the random seed
    if seed is not None:
        np.random.seed(seed)

    # Initialisation
    atm_state = ["IDLE"] * Num_atm # B(t): The ATM is in use, or idle
    Num_users = [0] * Num_atm # Q(t): The number of users in the system at time t

    # Store arrival times of waiting users for each ATM
    queues = [[] for _ in range(Num_atm)]

    Area_atm_state = 0 # AB
    Area_users = 0  # AQ

    total_energy = 0
    total_waiting_time = 0
    Num_started_service = 0
    total_response_time = 0
    Num_completed_users = 0
    current_customer_arrival = [None] * Num_atm

    # Initialise the event calendar
    first_arrival_time = np.random.exponential(1/arrival_rate)
    event_calendar = [(first_arrival_time, "arrival", None), (timesteps, "termination", None)]

    current_time = 0

    while True:
        # Find the next event and delete it from the event calendar
        next_index = min(range(len(event_calendar)), key=lambda i: event_calendar[i][0])
        event_time, event_type, server_id = event_calendar.pop(next_index)

        delta_time = event_time - current_time

        # Update AQ and AB
        Area_users += delta_time * sum(Num_users)
        busy_server = count_busy_servers(atm_state)
        Area_atm_state += delta_time * busy_server

        # Update energy consumption
        current_power = calculate_current_power(atm_state)

        total_energy += delta_time * current_power

        # Update the current time
        current_time = event_time

        if event_type == "arrival":

            arrival_time = current_time

            # Find the shortest queue
            chosen_server = choose_server(Num_users, policy)
            Num_users[chosen_server] += 1

            if atm_state[chosen_server] == "IDLE":
                atm_state[chosen_server] = "BUSY"

                # The user starts service immediately, so waiting time is 0
                total_waiting_time += 0
                Num_started_service += 1
                current_customer_arrival[chosen_server] = arrival_time

                departure_time = current_time + np.random.exponential(1 / service_rate)
                event_calendar.append((departure_time, "departure", chosen_server))

            else:
                # The user joins the queue of the chosen ATM
                queues[chosen_server].append(arrival_time)

            # Schedule the next arrival time
            next_arrival_time = current_time + np.random.exponential(1/arrival_rate)
            event_calendar.append((next_arrival_time, "arrival", None))

        elif event_type == "departure":
            Num_users[server_id] -= 1

            response_time = current_time - current_customer_arrival[server_id]
            total_response_time += response_time
            Num_completed_users += 1
            current_customer_arrival[server_id] = None

            if Num_users[server_id] > 0:
                # Next waiting customer starts service
                arrival_time_of_next_customer = queues[server_id].pop(0)

                waiting_time = current_time - arrival_time_of_next_customer
                total_waiting_time += waiting_time
                Num_started_service += 1
                current_customer_arrival[server_id] = arrival_time_of_next_customer

                # Schedule a new departure time
                departure_time = current_time + np.random.exponential(1 / service_rate)
                event_calendar.append((departure_time, "departure", server_id))

            else:
                atm_state[server_id] = "IDLE"

        elif event_type == "termination":
            Average_System_Size = Area_users/timesteps # L
            Utilization = Area_atm_state/(Num_atm * timesteps) # rho

            Average_Power = total_energy / timesteps
            Average_Waiting_Time = total_waiting_time / Num_started_service
            Average_Response_Time = total_response_time / Num_completed_users
            ERP = Average_Power * Average_Response_Time

            return Average_System_Size, Utilization, Average_Power, Average_Waiting_Time, Average_Response_Time, ERP

if __name__ == "__main__":
    Average_System_Size, Utilization, Average_Power, Average_Waiting_Time, Average_Response_Time, ERP = multi_ATM_simulator(
        Num_atm=5,
        arrival_rate=1,
        service_rate=1.5,
        timesteps=100,
        policy="NEVEROFF",
        seed=42
    )

    print("Simulation Finished")
    print("The Average System Size:", Average_System_Size)
    print("Utilization:", Utilization)
    print("Average Power:", Average_Power)
    print("Average Waiting Time:", Average_Waiting_Time)
    print("Average Response Time:", Average_Response_Time)
    print("ERP:", ERP)