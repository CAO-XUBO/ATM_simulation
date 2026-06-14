import numpy as np

def multi_ATM_simulator(Num_atm = 5, arrival_rate = 1, service_rate = 1.5, timesteps = 100, seed = 42):
    '''
    Num_atm: The number of ATM in the system
    arrival_rate: The arrival rate lambda
    service_rate: The service rate mu
    :return: Average_System_Size L and Utilization rho
    '''

    np.random.seed(seed)

    # Initialisation
    atm_state = [0] * Num_atm # B(t): The ATM is in use (1), or idle (0)
    Num_users = [0] * Num_atm # Q(t): The number of users in the system at time t

    Area_atm_state = 0 # AB
    Area_users = 0  # AQ


    # Initialise the event calendar
    first_arrival_time = np.random.exponential(1/arrival_rate)
    event_calendar = [(first_arrival_time, "arrival", None), (timesteps, "termination", None)]

    current_time = 0

    while True:
        # Find the next event and delete it from the event calendar
        next_index = min(range(len(event_calendar)), key=lambda i: event_calendar[i][0])
        event_time, event_type, server_id = event_calendar.pop(next_index)

        # Update AQ and AB
        Area_users += (event_time - current_time) * sum(Num_users)
        Area_atm_state += (event_time - current_time) * sum(atm_state)

        # Update the current time
        current_time = event_time

        if event_type == "arrival":

            # Find the shortest queue
            chosen_server = np.argmin(Num_users)
            Num_users[chosen_server] += 1

            if atm_state[chosen_server] == 0:
                atm_state[chosen_server] = 1
                departure_time = current_time + np.random.exponential(1 / service_rate)
                event_calendar.append((departure_time, "departure", chosen_server))

            # Schedule the next arrival time
            arrival_time = current_time + np.random.exponential(1/arrival_rate)
            event_calendar.append((arrival_time, "arrival", None))

        elif event_type == "departure":
            Num_users[server_id] -= 1
            if Num_users[server_id] > 0:
                # Schedule a new departure time
                departure_time = current_time + np.random.exponential(1 / service_rate)
                event_calendar.append((departure_time, "departure", server_id))
            else: atm_state[server_id] = 0

        elif event_type == "termination":
            Average_System_Size = Area_users/timesteps # L
            Utilization = Area_atm_state/(Num_atm * timesteps) # rho
            print("Simulation Finished")
            return Average_System_Size, Utilization

if __name__ == "__main__":
    Average_System_Size, Utilization = multi_ATM_simulator(Num_atm = 5,
                                                           arrival_rate = 1,
                                                           service_rate = 1.5,
                                                           timesteps = 100,
                                                           seed = 42)
    print("The Average System Size:", Average_System_Size)
    print("Utilization:", Utilization)