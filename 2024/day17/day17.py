with open("2024/day17/input.txt") as f:
    in_arr = f.read().split("\n\n")
    registers = in_arr[0].split("\n")
    a = int(registers[0].split(" ")[-1])
    b = int(registers[1].split(" ")[-1])
    c = int(registers[2].split(" ")[-1])
    instructions = in_arr[1].split(" ")[1].split(",")

output = []
instruction_pointer = 0
def get_combo_operand(operand: int) -> int:
        if operand < 4:
            return operand
        elif operand == 4:
            return a
        elif operand == 5:
            return b
        else:
            return c
instruction_pointer = 0
while instruction_pointer < len(instructions):
    instruction = instructions[instruction_pointer]
    operand = int(instructions[instruction_pointer + 1])
    if instruction == "0":
        a = a >> get_combo_operand(operand)
    elif instruction == "1":
        b = b ^ operand
    elif instruction == "2":
        b = get_combo_operand(operand) % 8
    elif instruction == "3":
        if a != 0:
            instruction_pointer = operand
            continue
    elif instruction == "4":
        b = b ^ c
    elif instruction == "5":
        output.append(str(get_combo_operand(operand) % 8))
    elif instruction == "6":
        b = a >> get_combo_operand(operand)
    else:
        c = a >> get_combo_operand(operand)
    instruction_pointer += 2
print(",".join(output))

def find_next(number, depth):
    number = number << 3
    numbers = []
    for i in range(8):
        num = number + i
        res = ((num % 8) ^ 3 ^ (num >> ((num % 8) ^ 3) ^ 5)% 8)
        if res == int(instructions[15 - depth]):
            numbers.append(num)
    if depth == 15:
        print(numbers)
        return
    for n in numbers:
        find_next(n, depth + 1)
    
        
find_next(0, 0)
        