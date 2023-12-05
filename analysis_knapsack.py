import os
import time
import tracemalloc
from knapsack_dp import knapsackdp
from knapsack_bnb import knapsackbnb

def load_dataset_from_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    W_line = lines[0].strip().split('=')[1].strip()
    val_line = lines[1].strip().split('=')[1].strip()
    wt_line = lines[2].strip().split('=')[1].strip()

    W = int(W_line)
    val = list(map(int, val_line[1:-1].split(',')))
    wt = list(map(int, wt_line[1:-1].split(',')))

    return W, val, wt

def measure_memory_usage(algorithm, *args, **kwargs):
    tracemalloc.start()

    algorithm(*args, **kwargs)

    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return current


dataset_folder = 'dataset/'

# Memuat dataset dari file
loaded_small_dataset = load_dataset_from_file(os.path.join(dataset_folder, 'dataset_small.txt'))
loaded_medium_dataset = load_dataset_from_file(os.path.join(dataset_folder, 'dataset_medium.txt'))
loaded_large_dataset = load_dataset_from_file(os.path.join(dataset_folder, 'dataset_large.txt'))

# Load dataset and measure time and memory for knapsack_dp and knapsack_bnb
for size, loaded_dataset in zip(['small', 'medium', 'large'], [loaded_small_dataset, loaded_medium_dataset, loaded_large_dataset]):
    W, val, wt = loaded_dataset

    print(f"\nDataset Size: {size.capitalize()}")

    # Knapsack DP
    dp_start_time = time.time()
    resultdp = knapsackdp(W, val, wt)
    dp_end_time = time.time()
    dp_time = dp_end_time - dp_start_time
    print(f"Time for knapsack_dp: {dp_time:.6f} seconds")

    # Knapsack BNB
    bnb_start_time = time.time()
    resultbnb, temp = knapsackbnb(W, val, wt)
    bnb_end_time = time.time()
    bnb_time = bnb_end_time - bnb_start_time
    print(f"Time for knapsack_bnb: {bnb_time:.6f} seconds")

    # Measure Memory Usage 
    dp_memory = measure_memory_usage(knapsackdp, W, val, wt)
    bnb_memory = measure_memory_usage(knapsackbnb, W, val, wt)
    print(f"\nMemory Usage for knapsack_dp: {dp_memory} bytes")
    print(f"Memory Usage for knapsack_bnb: {bnb_memory} bytes")

    # Check Result
    print("\nResult for knapsack_dp:", resultdp)
    print("Result for knapsack_bnb:", resultbnb)
