import numpy as np

def get_arrival_rate(Num_server, base_arrival_rate, arrival_model = "fixed", C = 0.3, alpha = 0.5):
    '''
    arrival_model
    fixed: a fixed arrival rate lambda
    fixed_scaling: lambda^n = n - C * n^alpha
    '''
    if arrival_model == "fixed":
        return base_arrival_rate

    elif arrival_model == "fixed_scaling":
        arrival_rate = Num_server - C * (Num_server ** alpha)

        if arrival_rate <= 0:
            raise ValueError("Arrival rate must be positive")
        return arrival_rate

    else:
        raise ValueError("Unknown arrival mode")

def generate_next_arrival_time(current_time, Num_server, base_arrival_rate, arrival_model, C, alpha):
    '''
    Generates the next arrival time
    '''

    arrival_rate = get_arrival_rate(
        Num_server=Num_server,
        base_arrival_rate=base_arrival_rate,
        arrival_model=arrival_model,
        C=C,
        alpha=alpha)

    # Calculate the actual arrival time
    inter_arrival_time = np.random.exponential(1/arrival_rate)
    actual_arrival_time = current_time + inter_arrival_time

    return actual_arrival_time
