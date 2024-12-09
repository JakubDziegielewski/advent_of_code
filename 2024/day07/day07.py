import numpy as np
from itertools import combinations_with_replacement, permutations
from time import time
result = 0
start = time()
with open("input.txt") as f:
    lines = f.readlines()
    solved = []
    for j, line in enumerate(lines):
        arr_one = line.strip().split(":")
        target = int(arr_one[0])
        numbers = list(map(int, arr_one[1].strip().split(" ")))
        operators = np.array(["*"] * (len(numbers) - 1))
        saved_results = [numbers[0]] * len(numbers)
        index = 0
        while "*" in operators:
            for i, operator in enumerate(operators[index:]):
                if operator == "*":
                    saved_results[index+1] = saved_results[index] * numbers[index + 1]
                else:
                    saved_results[index+1] = saved_results[index] + numbers[index + 1]
                index += 1
                if saved_results[index] > target:
                    indices = np.where(operators[:index] == "*")
                    last_index = indices[0][-1]
                    operators[last_index] = "+"
                    operators[last_index+1:].fill("*")
                    index = last_index
                    break
            else:
                if saved_results[-1] == target:
                    result += target
                    solved.append(j)
                    break
                indices = np.where(operators[:index] == "*")
                last_index = indices[0][-1]
                operators[last_index] = "+"
                operators[last_index+1:].fill("*")
                index = last_index
        else:
            if sum(numbers) == target:
                result += target  
                solved.append(j)  
            
        
print(result)

def to_base_3(n: int, length: int) -> str:
    if n == 0:
        return "0" * length
    digits = []
    while n:
        digits.append(str(n % 3))
        n //= 3
    result = ''.join(digits[::-1])
    return "0" * (length - len(result)) + result

def from_base_3(s):
    return int(s, 3)

lines = np.delete(lines, solved)

for line in lines:
    permutation = 0
    arr_one = line.strip().split(":")
    target = int(arr_one[0])
    numbers = list(map(int, arr_one[1].strip().split(" ")))
    saved_results = [numbers[0]] * len(numbers)
    index = 0
    while permutation < np.power(3, len(numbers) - 1):
        operators = to_base_3(permutation, len(numbers) - 1)
        if not "2" in operators:
            permutation += 1
            continue
        for operator in operators[index:]:
            if operator == "0":
                saved_results[index+1] = saved_results[index] * numbers[index + 1]
            elif operator == "1":
                saved_results[index+1] = saved_results[index] + numbers[index + 1]
            else:
                saved_results[index+1] = int(str(saved_results[index]) + str(numbers[index + 1]))
            index += 1
            if saved_results[index] > target:
                first_bits = operators[:index]
                last_bits = operators[index:]
                next_first_bits = from_base_3(first_bits) + 1
                next_first_bits = to_base_3(next_first_bits, index)
                first_array = np.array(list(first_bits))
                second_array = np.array(list(next_first_bits))
                if len(first_array) != len(second_array):
                    index = 0
                    next_first_bits += "0" * len(last_bits)
                    permutation = from_base_3(next_first_bits)
                else:
                    index = np.where(first_array != second_array)[0][0]
                    next_first_bits += "0" * len(last_bits)
                    permutation = from_base_3(next_first_bits)
                break
        else:
            if saved_results[-1] == target:
                result += target
                break
            first_bits = operators[:index]
            last_bits = operators[index:]
            next_first_bits = from_base_3(first_bits) + 1
            next_first_bits = to_base_3(next_first_bits, index)
            first_array = np.array(list(first_bits))
            second_array = np.array(list(next_first_bits))
            if len(first_array) != len(second_array):
                index = 0
                next_first_bits += "0" * len(last_bits)
                permutation = from_base_3(next_first_bits)
            else:
                index = np.where(first_array != second_array)[0][0]
                next_first_bits += "0" * len(last_bits)
                permutation = from_base_3(next_first_bits)
print(result)
end = time()
print(end - start)