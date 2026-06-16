from simulator import *
from Config import *

results = multi_ATM_simulator(
    Num_atm = NUM_SERVERS,
    arrival_rate = ARRIVAL_RATE,
    service_rate = SERVICE_RATE,
    timesteps = SIMULATION_TIME,
    seed = SEED
)

print(results)