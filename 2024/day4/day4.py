import numpy as np
import re

result = 0
array = np.zeros((140, 140), dtype='str')
with open("input.txt") as f:
    lines = f.readlines()
    for i, line in enumerate(lines):
        l = line.strip()
        number_of_xmas = len(re.findall(r'(?=(XMAS|SAMX))', l))
        result += number_of_xmas
        array[i] = np.array(list(l))

for line in array.T:
    l = "".join(line)
    number_of_xmas = len(re.findall(r'(?=(XMAS|SAMX))', l))
    result += number_of_xmas
    
rows, cols = array.shape
for offset in range(cols - 3):
    diag = array.diagonal(offset=offset)
    l = "".join(diag)
    number_of_xmas = len(re.findall(r'(?=(XMAS|SAMX))', l))
    result += number_of_xmas
    
for offset in range(1, rows - 3):
    diag = array.diagonal(offset=-offset)
    l = "".join(diag)
    number_of_xmas = len(re.findall(r'(?=(XMAS|SAMX))', l))
    result += number_of_xmas


array = np.fliplr(array)

for offset in range(cols - 3):
    diag = array.diagonal(offset=offset)
    l = "".join(diag)
    number_of_xmas = len(re.findall(r'(?=(XMAS|SAMX))', l))
    result += number_of_xmas
    
for offset in range(1, rows - 3):
    diag = array.diagonal(offset=-offset)
    l = "".join(diag)
    number_of_xmas = len(re.findall(r'(?=(XMAS|SAMX))', l))
    result += number_of_xmas

print(result)
result = 0

for offset in range(cols - 2):
    diag = array.diagonal(offset=offset)
    l = "".join(diag)
    number_of_xmas = re.finditer(r'(?=(MAS|SAM))', l)
    for n in number_of_xmas:
        begining = n.span()[0]
        down_letter = array[begining + 2][offset + begining]
        upper_letter = array[begining][offset + begining + 2]
        if down_letter == "M" and upper_letter == "S":
            result += 1
        elif down_letter == "S" and upper_letter == "M":
            result += 1
for offset in range(1, rows - 2):
    diag = array.diagonal(offset=-offset)
    l = "".join(diag)
    number_of_xmas = re.finditer(r'(?=(MAS|SAM))', l)
    for n in number_of_xmas:
        begining = n.span()[0]
        down_letter = array[offset + begining + 2][begining]
        upper_letter = array[offset + begining][begining + 2]
        if down_letter == "M" and upper_letter == "S":
            result += 1
        elif down_letter == "S" and upper_letter == "M":
            result += 1
print(result)

