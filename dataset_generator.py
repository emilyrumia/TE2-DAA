import os
import random

def generate_dataset(size):
    n = size
    W = random.randint(1, 1000)
    val = [random.randint(1, 100) for _ in range(n)]
    wt = [random.randint(1, 100) for _ in range(n)]
    return W, val, wt

def save_dataset_to_file(dataset, filename):
    W, val, wt = dataset

    with open(filename, 'w') as file:
        file.write(f'W = {W}\n')
        file.write(f'val = {val}\n')
        file.write(f'wt = {wt}\n')

# Membuat folder "dataset/" jika belum ada
dataset_folder = 'dataset/'
if not os.path.exists(dataset_folder):
    os.makedirs(dataset_folder)

# Ukuran kecil (100 barang)
small_dataset = generate_dataset(100)

# Ukuran sedang (1000 barang)
medium_dataset = generate_dataset(1000)

# Ukuran besar (10000 barang)
large_dataset = generate_dataset(10000)

# Menyimpan dataset ke dalam file di folder "dataset/"
save_dataset_to_file(small_dataset, os.path.join(dataset_folder, 'dataset_small.txt'))
save_dataset_to_file(medium_dataset, os.path.join(dataset_folder, 'dataset_medium.txt'))
save_dataset_to_file(large_dataset, os.path.join(dataset_folder, 'dataset_large.txt'))
