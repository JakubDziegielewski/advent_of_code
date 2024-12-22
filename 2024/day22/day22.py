import numpy as np
with open("2024/day22/input.txt") as f:
    lines = f.readlines()

"""result = 0
for line in lines:
    secret_num = int(line)
    for _ in range(2000):
        secret_num = (secret_num ^ (secret_num << 6)) % 16777216
        secret_num = secret_num ^ (secret_num >> 5) % 16777216
        secret_num = secret_num ^ (secret_num << 11) % 16777216
    result += secret_num
print(result)"""

sequences = np.zeros((19, 19, 19, 19), dtype=int)
result_one= 0
for line in lines:
    sold = np.zeros((19, 19, 19, 19), dtype=bool)
    secret_num = int(line)
    prices = [0] * 3
    for i in range(3):
        temp = secret_num % 10
        secret_num = (secret_num ^ (secret_num << 6)) % 16777216
        secret_num = secret_num ^ (secret_num >> 5) % 16777216
        secret_num = secret_num ^ (secret_num << 11) % 16777216
        units = secret_num % 10
        prices[i] = units - temp
    for j in range(3, 2000):
        temp = secret_num % 10
        secret_num = (secret_num ^ (secret_num << 6)) % 16777216
        secret_num = secret_num ^ (secret_num >> 5) % 16777216
        secret_num = secret_num ^ (secret_num << 11) % 16777216
        units = secret_num % 10
        prices.append(units - temp)
        if not sold[prices[0] + 9, prices[1] + 9, prices[2] + 9, prices[3] + 9]:
            sequences[prices[0] + 9, prices[1] + 9, prices[2] + 9, prices[3] + 9] += units
            sold[prices[0] + 9, prices[1] + 9, prices[2] + 9, prices[3] + 9] = True
        prices.pop(0)
    result_one += secret_num
print(result_one)
print(np.amax(sequences))