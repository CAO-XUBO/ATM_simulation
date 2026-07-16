import pandas as pd
import numpy as np
import os
from simulator import *
from Config import *

results = []

turn_off_threshold = range(0,6)
turn_on_threshold = range(-6,6)
c_values = [0.1, 0.3, 0.5]

for c in c_values:
    for T_i in turn_off_threshold:
        for T_o in turn_on_threshold:
            print("Start Simulation: c:", c, "T_i:", T_i, "T_o:", T_o)
            _, _, Average_Power, _, Average_Response_Time, ERP, Linear_cost_function = server_simulator(
                Num_server=NUM_SERVERS,
                arrival_rate=ARRIVAL_RATE,
                service_rate=SERVICE_RATE,
                timesteps=SIMULATION_TIME,
                setup_time=SETUP_TIME,
                policy="THRESHOLD",
                turn_off_threshold=T_i,
                turn_on_threshold=T_o,
                arrival_model="scaling",
                arrival_scale_C=c,
                arrival_alpha=ARRIVAL_ALPHA,
                seed=SEED,
            )

            results.append({
                "c_value": c,
                "T_i": T_i,
                "T_o": T_o,
                "Average_Power": Average_Power,
                "Average_Response_Time": Average_Response_Time,
                "ERP": ERP,
                "Linear_cost_function": Linear_cost_function,
            })

            print("Finish Simulation: c:", c, "T_i", T_i, "T_o", T_o)

results_df = pd.DataFrame(results)

output_filepath = "experiment_results"

if not os.path.exists(output_filepath):
    os.makedirs(output_filepath)

results_df.to_csv("experiment_results/threshold_experiment_results.csv")