import numpy as np

def get_arrival_rate(Num_server,
                     base_arrival_rate,
                     arrival_model = "fixed",
                     C = 0.3,
                     alpha = 0.5,
                     current_time = 0,
                     timesteps=100,
                     arrival_amplitude = 0.5):
    '''
    arrival_model
    fixed: a fixed arrival rate lambda

    fixed_scaling: lambda^n = n - C * n^alpha

    time_varying_scaling: lambda^n(t) = n - C * n^alpha * (1 + A * sin(2*pi*t/T))
    '''
    if arrival_model == "fixed":
        arrival_rate = base_arrival_rate

    elif arrival_model == "fixed_scaling":
        arrival_rate = Num_server - C * (Num_server ** alpha)

    elif arrival_model == "time_varying_scaling":
        if not (0 <= arrival_amplitude <= 1):
            raise ValueError("Arrival amplitude must be between 0 and 1")

        time_factor = 1 + arrival_amplitude * np.sin(2 * np.pi * current_time)

        arrival_rate = Num_server - C * (Num_server ** alpha) * time_factor

    else:
        raise ValueError("Unknown arrival mode")

    if arrival_rate <= 0:
        raise ValueError("Arrival rate must be positive")

    return arrival_rate

def get_max_arrival_rate(Num_server,
                         base_arrival_rate,
                         arrival_model="scaling_fixed",
                         C=0.3,
                         alpha = 0.5,
                         arrival_amplitude=0.5):
    if arrival_model == "fixed":
        return base_arrival_rate

    elif arrival_model == "fixed_scaling":

        max_arrival_rate = Num_server - C * (Num_server ** alpha)
        return max_arrival_rate

    elif arrival_model == "time_varying_scaling":
        if not (0 <= arrival_amplitude <= 1):
            raise ValueError("Arrival amplitude must be between 0 and 1")

        max_arrival_rate = Num_server - C * (Num_server ** alpha) * (1 - arrival_amplitude)
        return max_arrival_rate

    else:
        raise ValueError("Unknown arrival mode")


def generate_next_arrival_time(current_time,
                               Num_server,
                               base_arrival_rate,
                               arrival_model,
                               C,
                               alpha,
                               timesteps=100,
                               arrival_amplitude=0.5):
    """
    Generates the next arrival time
    """

    if arrival_model in ["fixed", "fixed_scaling"]:

        arrival_rate = get_arrival_rate(
            Num_server=Num_server,
            base_arrival_rate=base_arrival_rate,
            arrival_model=arrival_model,
            C=C,
            alpha=alpha
        )

        inter_arrival_time = np.random.exponential(1 / arrival_rate)

        return current_time + inter_arrival_time

    elif arrival_model == "time_varying_scaling":

        lambda_max = get_max_arrival_rate(
            Num_server=Num_server,
            base_arrival_rate=base_arrival_rate,
            arrival_model=arrival_model,
            C=C,
            alpha=alpha,
            arrival_amplitude=arrival_amplitude
        )

        candidate_time = current_time

        while True:
            candidate_time += np.random.exponential(1 / lambda_max)

            if candidate_time > timesteps:
                return None

            current_arrival_rate = get_arrival_rate(
                Num_server=Num_server,
                base_arrival_rate=base_arrival_rate,
                arrival_model=arrival_model,
                C=C,
                alpha=alpha,
                current_time=candidate_time,
                timesteps=timesteps,
                arrival_amplitude=arrival_amplitude
            )

            accept_probability = current_arrival_rate / lambda_max

            if np.random.random() <= accept_probability:
                return candidate_time

    else:
        raise ValueError("Unknown arrival model")
