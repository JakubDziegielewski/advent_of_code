import numpy as np
from time import time

class Field:
    def __init__(self, symbol: str, row:int, column: int):
        self.symbol = symbol
        self.row = row
        self.column = column
        self.id = (row, column)
        self.fences = np.array([0, 0, 0, 0])
    def add_fence(self, index: int) -> None:
        self.fences[index] = 1
    def __repr__(self) -> str:
        return f"{self.symbol}, ({self.row}, {self.column})"

start = time()
ids = dict()
with open("input.txt") as f:
    lines = f.readlines()
size = len(lines)
fields = np.zeros((size, size), dtype=Field)

def check_two_fields(field_one: Field, field_two: Field) -> None:
    current_id = field_one.id
    other_id = field_two.id
    if current_id != other_id:
        ids[other_id] += ids[current_id]
        for field in ids[current_id]:
            field.id = other_id
        ids.pop(current_id)
        
for i, line in enumerate(lines):
    for j, char in enumerate(line.strip()):
        fields[i, j] = Field(char, i, j)
        ids[fields[i][j].id] = [fields[i][j]]
        if i == size - 1:
            fields[i, j].add_fence(2)
        if j == size - 1:
            fields[i, j].add_fence(1)
        if i == 0:
            fields[i, j].add_fence(0)
        elif fields[i, j].symbol == fields[i - 1, j].symbol:
            check_two_fields(fields[i, j], fields[i - 1, j])
        else:
            fields[i, j].add_fence(0)
            fields[i - 1, j].add_fence(2)
        if j == 0:
            fields[i,j].add_fence(3)
        elif fields[i, j].symbol == fields[i, j - 1].symbol:
            check_two_fields(fields[i,j], fields[i, j - 1])
        else:
            fields[i, j].add_fence(3)
            fields[i, j - 1].add_fence(1)

result = 0
for v in ids.values():
    result += len(v) * sum([sum(x.fences) for x in v])
print(result)

result = 0
for v in ids.values():
    sides = []
    number_of_sides = 0
    for item in v:
        indices = np.where(item.fences == 1)
        for index in indices[0]:
                sides.append((item.row, item.column, index))
        number_of_sides = 0
    for s in sides:
        if s[2] % 2 == 0:
            if (s[0], s[1] + 1, s[2]) not in sides:
                number_of_sides += 1
        else:
            if (s[0] + 1, s[1], s[2]) not in sides:
                number_of_sides += 1
    result += len(v) * number_of_sides
print(result)
end = time()
print(end - start)