import random
import math
'''
This script implements a probabilistic bitmap sketch for single-flow spread estimation
'''
class ProbabilisticBitmapSketch:
    def __init__(self, m, p):
        self.m = m
        self.p = p
        self.bitmap = [0] * m
        self.hash_fn = 51
        self.hash_fn2 = random.randint(1000000,10000000)

    def reset_bitmap(self):
        self.bitmap = [0] * self.m

    def record_flow(self, flow_id):
        hash_value = (flow_id * self.hash_fn) % self.m
        if hash_value < (len(self.bitmap)*self.p):
            # Use another hash function!
            hash_value = (flow_id ^ self.hash_fn2) % self.m
            self.bitmap[hash_value] = 1

    def estimate_spread(self):
        num_zeros = self.bitmap.count(0)

        percent_zeros = num_zeros/len(self.bitmap)

        if percent_zeros == 0:
            percent_zeros = 1/len(self.bitmap)

        estimated_spread = -(len(self.bitmap)/self.p)*math.log2(percent_zeros)
        return estimated_spread


if __name__ == '__main__':
    # Set the number of bits in the bitmap and sampling probability
    m = 10000
    p = 0.1

    # Initialize the ProbabilisticBitmapSketch
    prob_bitmap_sketch = ProbabilisticBitmapSketch(m, p)

    # List of flow spreads
    flow_spreads = [100,1000,10000,100000, 1000000]

    flow_arrays = []
    for flow_spread in flow_spreads:
        flows = []
        for index in range(flow_spread):
            element_id = random.randrange(1000000000)
            flows.append(element_id)

        flow_arrays.append(flows)

    # Record flows and estimate spread for each flow
    estimated_spreads = []
    for i,flows in enumerate(flow_arrays):
        for flow in flows:
            prob_bitmap_sketch.record_flow(flow)
        true_spread = flow_spreads[i]
        estimated_spread = prob_bitmap_sketch.estimate_spread()
        prob_bitmap_sketch.reset_bitmap()
        estimated_spreads.append(estimated_spread)

    #Write to file
    with open("prob_bitmap.txt", "w") as file:
        for i,spread in enumerate(flow_spreads):
            file.write(f"{spread} {estimated_spreads[i]} \n")