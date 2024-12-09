import re

result = 0
with open("input.txt") as f:
    text = f.read()
    for match in re.finditer("mul\(\d+,\d+\)", text):
        numbers = match.group()[4:-1].split(",")
        result += int(numbers[0]) * int(numbers[1])
print(result)

result = 0
mul_enabled = True

with open("input.txt") as f:
    text = f.read()
    for match in re.finditer("mul\(\d+,\d+\)|do\(\)|don't\(\)", text):
        instruction = match.group()
        if instruction == "do()":
            mul_enabled = True
        elif instruction == "don't()":
            mul_enabled = False
        elif mul_enabled:
            numbers = match.group()[4:-1].split(",")
            result += int(numbers[0]) * int(numbers[1])
print(result)