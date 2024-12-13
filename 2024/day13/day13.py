from time import time

with open("input.txt") as f:
    lines = f.readlines()


start = time() 
result = 0
for i in range(0, len(lines), 4):
    array_one = lines[i].split()
    array_two = lines[i + 1].split()
    array_three = lines[i + 2].split()
    m11, m12 = int(array_one[2][2:-1]), int(array_one[3][2:])
    m21, m22 = int(array_two[2][2:-1]), int(array_two[3][2:])
    p1, p2 = int(array_three[1][2:-1]), int(array_three[2][2:])
    a2 = (p2 * m11 - p1 * m12) / (m11 * m22 - m12 * m21)
    if a2.is_integer():
        a1 = (p1 - a2 * m21) / m11
        if a1.is_integer():
            result += 3 * int(a1) + int(a2)
print(result)
result = 0
for i in range(0, len(lines), 4):
    array_one = lines[i].split()
    array_two = lines[i + 1].split()
    array_three = lines[i + 2].split()
    m11, m12 = int(array_one[2][2:-1]), int(array_one[3][2:])
    m21, m22 = int(array_two[2][2:-1]), int(array_two[3][2:])
    p1, p2 = 10000000000000 + int(array_three[1][2:-1]), 10000000000000 + int(array_three[2][2:])
    a2 = (p2 * m11 - p1 * m12) / (m11 * m22 - m12 * m21)
    if a2.is_integer():
        a1 = (p1 - a2 * m21) / m11
        if a1.is_integer():
            result += 3 * int(a1) + int(a2)
end = time()
print(result)
print(end - start)