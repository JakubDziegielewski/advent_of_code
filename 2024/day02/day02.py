import numpy as np

safe_lines = 0
lines = []
with open("input.txt") as f:
    lines=f.readlines()
for line in lines:
    array = np.fromstring(line, dtype=int, sep=' ')
    if array[0] > array[1]:
        array = np.flip(array)
    for i in range(len(array) - 1):
        diff = array[i + 1] - array[i]
        if diff < 1 or diff > 3:
            break
    else:
        safe_lines += 1
print(safe_lines)


safe_lines = 0
for line in lines:
    array = np.fromstring(line, dtype=int, sep=' ')
    for i in range(len(array)):
        new_array = np.delete(array, i)
        if new_array[0] > new_array[1]:
            new_array = np.flip(new_array)
        for i in range(len(new_array) - 1):
            diff = new_array[i + 1] - new_array[i]
            if diff < 1 or diff > 3:
                break
        else:
            safe_lines += 1
            break
print(safe_lines)
