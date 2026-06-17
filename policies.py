import numpy as np

def choose_server_neveroff(Num_users, atm_state):
    return np.argmin(Num_users)

def choose_server_instantoff(Num_users, atm_state):
    return np.argmin(Num_users)

def get_policy_functions(policy):
    if policy == "NEVEROFF":
        return {
            "choose_server": choose_server_neveroff,
            "idle_state_after_departure": "IDLE",
            "initial_state": "IDLE"
        }

    elif policy == "INSTANTOFF":
        return {
            "choose_server": choose_server_instantoff,
            "idle_state_after_departure": "OFF",
            "initial_state": "OFF"
        }

    else:
        raise ValueError("Unknown policy")