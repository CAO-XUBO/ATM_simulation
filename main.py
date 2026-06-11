import numpy as np

# Initialisation
atm_state = 0 # B(t): The ATM is in use (1), or idle (0)
Num_users = 0 # Q(t): The number of users in the system at time t

Area_atm_state = 0 # AB
Area_users = 0  # AQ

arrival_rate = 1.0 # lambda
service_rate = 1.5 # mu
timesteps = 100

first_arrival_time = np.random.exponential(1/arrival_rate)
event_calendar = [(first_arrival_time, "arrival"), (timesteps, "termination")]

current_time = 0

while True:

    # Find the next event
    next_index = min(range(len(event_calendar)), key=lambda i: event_calendar[i][0])
    event_time, event_type = event_calendar.pop(next_index)

    # Update AQ and AB
    Area_users = Area_users + (event_time - current_time) * Num_users
    Area_atm_state = Area_atm_state + (event_time - current_time) * atm_state

    # Update the current time
    current_time = event_time

    if event_type == "arrival":
        Num_users = Num_users + 1
        if atm_state == 0:
            atm_state = 1
            # Schedule a new departure time
            departure_time = current_time + np.random.exponential(1/service_rate)
            event_calendar.append((departure_time, "departure"))

        # Schedule the next arrival time
        arrival_time = current_time + np.random.exponential(1/arrival_rate)
        event_calendar.append((arrival_time, "arrival"))

    elif event_type == "departure":
        Num_users = Num_users - 1
        if Num_users > 0:
            # Schedule a new departure time
            departure_time = current_time + np.random.exponential(1 / service_rate)
            event_calendar.append((departure_time, "departure"))
        else: atm_state = 0

    elif event_type == "termination":
        Average_System_Size = Area_users/timesteps # L
        Utilization = Area_atm_state/timesteps # rho

        print(Average_System_Size, Utilization)
        break