from simulator import *
from Config import *

Average_System_Size, Utilization, Average_Power, Average_Waiting_Time, Average_Response_Time, ERP  = server_simulator(
        Num_server = 5,
        arrival_rate = ARRIVAL_RATE,
        service_rate = SERVICE_RATE,
        timesteps = SIMULATION_TIME,
        policy = "INSTANTOFF",  # "INSTANTOFF", "NEVEROFF"
        seed = 42)

print("Simulation Finished")
print("The Average System Size:", Average_System_Size)
print("Utilization:", Utilization)
print("Average Power:", Average_Power)
print("Average Waiting Time:", Average_Waiting_Time)
print("Average Response Time:", Average_Response_Time)
print("ERP:", ERP)