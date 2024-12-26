with open("2024/day24/input.txt") as f:
    arr_one = f.read().split("\n\n")
    inputs = arr_one[0].split("\n")
    gates = arr_one[1].split("\n")

wires = dict()
for input_wire in inputs:
    arr = input_wire.split(":")
    wires[arr[0]] = int(arr[1])

class Gate:
    def __init__(self, input_one, operation, input_two, output):
        self.input_one = input_one
        self.input_two = input_two
        self.operation = operation
        self.output = output
        self.output_calculated = False
    def calculate_output(self):
        if self.output == "z09":
            pass
        self.output_calculated = True
        in_one = wires[self.input_one]
        in_two = wires[self.input_two]
        if self.operation == "AND":
            return in_one & in_two
        elif self.operation == "OR":
            return in_one | in_two
        else:
            return in_one ^ in_two
    def __lt__(self, other):
        return self.output < other.output
    
    def __eq__(self, other):
        first_condition = self.input_one == other.input_one
        second_condition = self.input_two == other.input_two
        third_condition = self.input_one == other.input_two
        fourth_condition = self.input_two == other.input_one
        if first_condition and second_condition:
            return self.operation == other.operation and self.output == other.output
        elif third_condition and fourth_condition:
            return self.operation == other.operation and self.output == other.output
    def __repr__(self):
        return f"{self.input_one} {self.operation} {self.input_two} -> {self.output}"
        
reverse = dict()
logic_gates = dict()
for gate in gates:
    arr_one = gate.split(" -> ")
    arr_two = arr_one[0].split(" ")
    if arr_two[0] > arr_two[2]:
        temp = arr_two[0]
        arr_two[0] = arr_two[2]
        arr_two[2] = temp
    logic_gates[arr_two[0], arr_two[1], arr_two[2]] = Gate(arr_two[0], arr_two[1], arr_two[2], arr_one[1])
    reverse[arr_one[1]] = [arr_two[0], arr_two[1], arr_two[2]]

calculated_outputs = 0
result = 0
while calculated_outputs < len(gates):
    for logic_gate in logic_gates.values():
        if logic_gate.output_calculated:
            continue
        if logic_gate.input_one in wires.keys() and logic_gate.input_two in wires.keys():
            out = logic_gate.calculate_output()
            wires[logic_gate.output] = out
            if logic_gate.output[0] == "z" and out == 1:
                result += 1 << int(logic_gate.output[1:])
            calculated_outputs += 1
print(result)

p = None
wrong_outputs = []
z_outputs = sorted([x for x in wires if x[0] == "z"])

for z in z_outputs:
    if p is None:
        xor_one = reverse[z]
        if xor_one != ['x00', 'XOR', 'y00']:
            wrong_outputs.append(z)
            wrong_outputs.append(logic_gates['x00', 'XOR', 'y00'].output)
            temp = logic_gates['x00', 'XOR', 'y00'].output
            logic_gates['x00', 'XOR', 'y00'].output = z
            logic_gates[*xor_one].output = temp
        p = logic_gates['x00', 'AND', 'y00'].output
    elif int(z[1:]) < 45:
        xor_one = reverse[z]
        number = z[1:]
        if xor_one[1] != "XOR":
            wrong_outputs.append(z)
            out_one = logic_gates["x" + number, "XOR", "y" + number].output
            if p < out_one:
                wrong_outputs.append(logic_gates[p, "XOR", out_one].output)
                temp = logic_gates[p, "XOR", out_one].output
                logic_gates[p, "XOR", out_one].output = z
                logic_gates[*xor_one].output = temp
            else:
                wrong_outputs.append(logic_gates[out_one, "XOR", p].output)
                temp = logic_gates[out_one, "XOR", p].output
                logic_gates[out_one, "XOR", p].output = z
                logic_gates[*xor_one].output = temp
        else:
            if p == xor_one[0]:
                if reverse[xor_one[2]] != ["x" + number, "XOR", "y" + number]:
                    wrong_outputs.append(xor_one[2])
                    wrong_outputs.append(logic_gates["x" + number, "XOR", "y" + number].output)
                    temp = logic_gates["x" + number, "XOR", "y" + number].output
                    logic_gates["x" + number, "XOR", "y" + number].output = xor_one[2]
                    logic_gates[*reverse[xor_one[2]]].output = temp
            elif p == xor_one[2]:
                if reverse[xor_one[0]] != ["x" + number, "XOR", "y" + number]:
                    wrong_outputs.append(xor_one[0])
                    wrong_outputs.append(logic_gates["x" + number, "XOR", "y" + number].output)
                    temp = logic_gates["x" + number, "XOR", "y" + number].output
                    logic_gates["x" + number, "XOR", "y" + number].output = xor_one[0]
                    logic_gates[*reverse[xor_one[0]]].output = temp
            else:
                wrong_outputs.append(z)
                out_one = logic_gates["x" + number, "XOR", "y" + number].output
                if p < out_one:
                    wrong_outputs.append(logic_gates[p, "XOR", out_one].output)
                    temp = logic_gates[p, "XOR", out_one].output
                    logic_gates[p, "XOR", out_one].output = z
                    logic_gates[*xor_one].output = temp
                    reverse[z] = [p, "XOR", out_one]
                    reverse[temp] = xor_one
                else:
                    wrong_outputs.append(logic_gates[out_one, "XOR", p].output)
                    temp = logic_gates[out_one, "XOR", p].output
                    logic_gates[out_one, "XOR", p].output = z
                    logic_gates[*xor_one].output = temp
                    reverse[z] = [p, "XOR", out_one]
                    reverse[temp] = xor_one
        and_output = logic_gates["x" + number, "AND", "y" + number].output
        xor_output = logic_gates["x" + number, "XOR", "y" + number].output
        if p < xor_output:
            second_and = logic_gates[p, "AND", xor_output].output
        else:
            second_and = logic_gates[xor_output, "AND", p].output
        if and_output < second_and:
            p = logic_gates[and_output, "OR", second_and].output
        else:
            p = logic_gates[second_and, "OR", and_output].output
print(",".join(sorted(wrong_outputs)))