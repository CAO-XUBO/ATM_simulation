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

    Num_idle_servers = count_state(server_state, "IDLE")
    Num_setup_servers = count_state(server_state, "SETUP")
    Num_off_servers = count_state(server_state, "OFF")

    if queue_length == 0:
        return False

    if Num_idle_servers > 0:
        return False

    if Num_off_servers == 0:
        return False

    if Num_setup_servers >= queue_length:
        return False

    return True


def should_start_setup_threshold(central_queue, server_state, turn_on_threshold):
    '''
    The turn-on rule for Threshold policy
    turn_on_threshold: T_o
    '''

    Num_idle_servers = count_state(server_state, "IDLE")
    Num_off_servers = count_state(server_state, "OFF")

    if Num_off_servers == 0:
        return False

    # Case I: when T_o is positive, the policy focus on the number of idle servers
    if turn_on_threshold > 0:
        if Num_idle_servers < turn_on_threshold:
            return True
        else:
            return False

    # Case II: when T_o is negative, the policy focus on the length of central queue
    else:
        queue_length = len(central_queue)
        queue_threshold = abs(turn_on_threshold)

        if queue_length >= queue_threshold:
            return True
        else:
            return False

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