import numpy as np
from typing import Tuple
SIZE = 50


with open("input.txt") as f:
    lines = f.readlines()
warehouse = np.array([list(line.strip()) for line in lines[:SIZE]])
condition = warehouse == "@"
start = np.where(condition)
row = start[0][0]
column = start[1][0]
moves = "".join([line.strip() for line in lines[SIZE + 1:]])

move_directions = {
    ">": [0, 1],
    "v": [1, 0],
    "<": [0, -1],
    "^": [-1, 0]
}
def try_moving(row: int, column:int, move: str) -> Tuple[int, int]:
    direction = move_directions[move]
    next_row = row + direction[0]
    next_column = column + direction[1]
    while warehouse[next_row][next_column] == "O":
        next_row += direction[0]
        next_column += direction[1]
    if warehouse[next_row][next_column] == ".":
        warehouse[row][column] = "."
        warehouse[next_row][next_column] = "O"
        warehouse[row + direction[0]][column + direction[1]] = "@"
        return row + direction[0], column + direction[1]
    return row, column
for move in moves:
    row, column = try_moving(row, column, move)

result = 0
it = np.nditer(warehouse, flags=['multi_index'])
for field in it:
    if field == "O":
        result += it.multi_index[0] * 100 + it.multi_index[1]
print(result)
