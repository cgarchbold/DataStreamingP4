import math
import random
'''

'''
class HyperLogLog:
    def __init__(self, m):
        self.m = m
        self.registers = [0] * m
        self.hash_fn = 37 #random.randint(1000000,10000000)
        self.hash_fn2 = random.randint(1000000,10000000)

    def geometric_hash(self,flow_id):
        # convert to binary, remove the 0b
        binary = bin(flow_id)[2:]

        g = 8 - len(binary)

        return g
    

    def reset_registers(self):
        self.registers = [0] * self.m

    def record_flow(self, flow_id):
        hash_value = (flow_id * self.hash_fn) % self.m
        g = self.geometric_hash(hash_value)
        g_prime = g+1
        hash_value = (flow_id ^ self.hash_fn2) % self.m
        self.registers[hash_value] = max(self.registers[hash_value], g_prime)

    def estimate_spread(self):
        estimated_flow_spread = 0
        alpha = 0.7213/(1 + 1.079/self.m)

        # Calculating estimated flow using formula for HLL Sketch querying
        for register_value in self.registers:
            estimated_flow_spread += 1/(2 ** register_value)
        estimated_flow_spread = estimated_flow_spread ** -1
        estimated_flow_spread = estimated_flow_spread * (self.m ** 2) * alpha

        return estimated_flow_spread

if __name__ == '__main__':
    # Set the number of registers for HLL
    m = 256

    # Initialize the HyperLogLog
    hll = HyperLogLog(m)

    # List of flow spreads
    flow_spreads = [1000, 10000, 100000, 1000000]

    flow_arrays = []
    for flow_spread in flow_spreads:
        flows = []
        for index in range(flow_spread):
            element_id = random.randrange(10000000)
            flows.append(element_id)

        flow_arrays.append(flows)

    # Record flows and estimate spread for each flow
    estimated_spreads = []
    for i,flows in enumerate(flow_arrays):
        for flow in flows:
            hll.record_flow(flow)
        true_spread = flow_spreads[i]
        estimated_spread = hll.estimate_spread()
        hll.reset_registers()
        estimated_spreads.append(estimated_spread)

    #Write to file
    with open("hll.txt", "w") as file:
        for i,spread in enumerate(flow_spreads):
            file.write(f"{spread} {estimated_spreads[i]} \n")
