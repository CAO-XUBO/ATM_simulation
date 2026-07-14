import numpy as np

def count_state(server_state, target_state):
    return sum(1 for state in server_state if state == target_state)

def choose_off_server(server_state):
    for i, state in enumerate(server_state):
        if state == "OFF":
            return i
    return None

def should_start_setup_neveroff(central_queue, server_state):
    '''
    The turn-on rule for NEVEROFF policy
    '''
    return False

def should_start_setup_instantoff(central_queue, server_state):
    '''
    The turn-on rule for INSTANT policy
    '''
    queue_length = len(central_queue)

    idle_servers = count_state(server_state, "IDLE")
    setup_servers = count_state(server_state, "SETUP")
    off_servers = count_state(server_state, "OFF")

    if queue_length == 0:
        return False

    if idle_servers > 0:
        return False

    if off_servers == 0:
        return False

    if setup_servers >= queue_length:
        return False

    return True

def get_policy_functions(policy):
    if policy == "NEVEROFF":
        return {
            "idle_state_after_departure": "IDLE",
            "initial_state": "IDLE",
            "should_start_setup": should_start_setup_neveroff,
            "choose_off_server": choose_off_server
        }

    elif policy == "INSTANTOFF":
        return {
            "idle_state_after_departure": "OFF",
            "initial_state": "OFF",
            "should_start_setup": should_start_setup_instantoff,
            "choose_off_server": choose_off_server
        }

    else:
        raise ValueError("Unknown policy")