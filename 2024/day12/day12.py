import numpy as np

class Field:
    def __init__(self, symbol: str, row:int, column: int):
        self.symbol = symbol
        self.row = row
        self.column = column
        self.top_left = (row, column)
        self.fences = 0
    def __repr__(self) -> str:
        return f"{self.symbol}, ({self.row}, {self.column})"

top_lefts = dict()
with open("input.txt") as f:
    lines = f.readlines()
    size = len(lines)
    fields = np.zeros((size, size), dtype=Field)
    for i, line in enumerate(lines):
        for j, char in enumerate(line.strip()):
            fields[i][j] = Field(char, i, j)
            top_lefts[fields[i][j].top_left] = [fields[i][j]]
            if i == size - 1:
                fields[i, j].fences += 1
            if j == size - 1:
                fields[i, j].fences += 1
            if i == 0:
                fields[i,j].fences += 1
            elif fields[i][j].symbol == fields[i - 1, j].symbol:
                current_top_left = fields[i, j].top_left
                other_top_left = fields[i - 1, j].top_left
                if other_top_left[0] < current_top_left[0]:
                    top_lefts[other_top_left] += top_lefts[current_top_left]
                    for field in top_lefts[current_top_left]:
                        field.top_left = other_top_left
                    top_lefts.pop(current_top_left)
                elif other_top_left[0] == current_top_left[0] and other_top_left[1] < current_top_left[1]:
                    top_lefts[other_top_left] += top_lefts[current_top_left]
                    for field in top_lefts[current_top_left]:
                        field.top_left = other_top_left
                    top_lefts.pop(current_top_left)
                elif other_top_left[0] > current_top_left[0]:
                    top_lefts[current_top_left] += top_lefts[other_top_left]
                    for field in top_lefts[other_top_left]:
                        field.top_left = current_top_left
                    top_lefts.pop(other_top_left)
                elif other_top_left[0] == current_top_left[0] and other_top_left[1] > current_top_left[1]:
                    top_lefts[current_top_left] += top_lefts[other_top_left]
                    for field in top_lefts[other_top_left]:
                        field.top_left = current_top_left
                    top_lefts.pop(other_top_left)
            else:
                fields[i, j].fences += 1
                fields[i - 1, j].fences += 1
            if j == 0:
                fields[i,j].fences += 1
            elif fields[i][j].symbol == fields[i, j - 1].symbol:
                current_top_left = fields[i, j].top_left
                other_top_left = fields[i, j - 1].top_left
                if other_top_left[0] < current_top_left[0]:
                    top_lefts[other_top_left] += top_lefts[current_top_left]
                    for field in top_lefts[current_top_left]:
                        field.top_left = other_top_left
                    top_lefts.pop(current_top_left)
                elif other_top_left[0] == current_top_left[0] and other_top_left[1] < current_top_left[1]:
                    top_lefts[other_top_left] += top_lefts[current_top_left]
                    for field in top_lefts[current_top_left]:
                        field.top_left = other_top_left
                    top_lefts.pop(current_top_left)
                elif other_top_left[0] > current_top_left[0]:
                    top_lefts[current_top_left] += top_lefts[other_top_left]
                    for field in top_lefts[other_top_left]:
                        field.top_left = current_top_left
                    top_lefts.pop(other_top_left)
                elif other_top_left[0] == current_top_left[0] and other_top_left[1] > current_top_left[1]:
                    top_lefts[current_top_left] += top_lefts[other_top_left]
                    for field in top_lefts[other_top_left]:
                        field.top_left = current_top_left
                    top_lefts.pop(other_top_left)
            else:
                fields[i, j].fences += 1
                fields[i, j - 1].fences += 1

result = 0
for k in top_lefts.keys():
    result += len(top_lefts[k]) * sum([x.fences for x in top_lefts[k]])
print(result)

