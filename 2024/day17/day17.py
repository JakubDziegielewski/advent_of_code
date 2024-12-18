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

def get_combo(operand, reg_one, reg_two, reg_three):
    if operand < 4:
        return operand
    elif operand == 4:
        return reg_one
    elif operand == 5:
        return reg_two
    else:
        return reg_three
    
results = []
def find_next(number, depth):
    number = number << 3
    numbers = []
    for i in range(8):
        reg_two, reg_three = 0, 0
        init_num = number + i
        reg_one = init_num
        instruction_pointer = 0
        while instruction_pointer < len(instructions):
            instruction = instructions[instruction_pointer]
            operand = int(instructions[instruction_pointer + 1])
            if instruction == "0":
                reg_one = reg_one >> get_combo(operand, reg_one, reg_two, reg_three)
            elif instruction == "1":
                reg_two = reg_two ^ operand
            elif instruction == "2":
                reg_two = get_combo(operand, reg_one, reg_two, reg_three) % 8
            elif instruction == "3":
                pass
            elif instruction == "4":
                reg_two = reg_two ^ reg_three
            elif instruction == "5":
                res = get_combo(operand, reg_one, reg_two, reg_three) % 8
            elif instruction == "6":
                reg_two = reg_one >> get_combo(operand, reg_one, reg_two, reg_three)
            else:
                reg_three = reg_one >> get_combo(operand, reg_one, reg_two, reg_three)
            instruction_pointer += 2
        if res == int(instructions[15 - depth]):
            numbers.append(init_num)
            if depth == 15:
                results.append(init_num)
                return
    for n in numbers:
        find_next(n, depth + 1)
    
        
find_next(0, 0)
print(min(results))
        