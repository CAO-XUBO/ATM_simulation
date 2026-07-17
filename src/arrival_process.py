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
