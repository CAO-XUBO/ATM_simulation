
'''The main task of this code file is using the Nelder Mead Method to find the optimal threshold T_i and T_o'''
import numpy as np
import pandas as pd
from scipy.optimize import minimize

from simulator import server_simulator
from src.Config import *

## Experimental Settings
Num_servers = NUM_SERVERS
arrival_rate = ARRIVAL_RATE
service_rate = SERVICE_RATE
simulation_time = SIMULATION_TIME
setup_time = SETUP_TIME

POLICY = "THRESHOLD"

ARRIVAL_MODEL = "fixed_scaling"
ARRIVAL_SCALE_C = 0.3
ARRIVAL_ALPHA = 0.5
policy = "THRESHOLD"

# Choose which objective to optimise:
# "exact"  -> use Objective_Exact
# "little" -> use Objective_Little
OBJECTIVE_TYPE = "little"

# Common random numbers
OPTIMIZATION_SEEDS = list(range(100, 110))

# Cache for repeated rounded threshold combinations
objective_cache = {}

# Store evaluated points for later analysis
evaluation_records = []

def threshold_constraints(T_i, T_o):
    """
    Check whether a threshold combination is feasible.
    T_i: turn-off threshold
    T_o: turn-on threshold
    Current policy interpretation:
    - T_i should be non-negative.
    - T_i cannot exceed number of servers.
    - T_o can be negative or non-negative.
      If T_o < 0, abs(T_o) is interpreted as a queue-length threshold.
      If T_o >= 0, T_o is interpreted as an idle-server threshold.
    """

    if T_i < 0:
        return False

    if T_i > NUM_SERVERS:
        return False

    if T_o < -20 or T_o > NUM_SERVERS:
        return False

    # If T_o >= 0 and T_i <= T_o, turn-on and turn-off rules may conflict.
    if T_o >= 0 and T_i <= T_o:
        return False

    return True