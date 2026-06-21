from simulator import *
from Config import *

results = server_simulator(Num_server=NUM_SERVERS, arrival_rate=ARRIVAL_RATE, service_rate=SERVICE_RATE,
                           timesteps=SIMULATION_TIME, seed=SEED)

print(results)