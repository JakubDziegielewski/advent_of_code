import numpy as np
from bisect import insort
from time import time

keys = []
locks = []
with open("2024/day25/input.txt") as f:
    schemas = f.read().split("\n\n")
start = time()
for schema in schemas:
    lock = schema[0] == "#"
    columns = np.array(list(map(list, schema.split("\n"))))
    final_schema = np.sum(columns == "#", axis=0) - 1
    if lock:
        insort(locks, final_schema, key=lambda x: tuple(x))
    else:
        insort(keys, final_schema, key=lambda x: tuple(x))
result = 0
for lock in locks:
    for key in keys:
        result_sum = lock + key
        if result_sum[0] > 5:
            break
        if all(result_sum < 6):
            result += 1
end = time()
print(result)
print(end - start)