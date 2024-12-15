from time import time
import numpy as np
from typing import Tuple
SIZE = 50


with open("input.txt") as f:
    lines = f.readlines()
start = time()
warehouse = np.zeros((SIZE, SIZE * 2), dtype=str)
for i, line in enumerate(lines[:SIZE]):
    for j, char in enumerate(line.strip()):
        real_column = 2 * j
        if char == "O":
            warehouse[i, real_column] = "["
            warehouse[i, real_column + 1] = "]"
        elif char == "@":
            row = i
            column = real_column
            warehouse[i, real_column] = "@"
            warehouse[i, real_column + 1] = "."
        else:
            warehouse[i, real_column] = char
            warehouse[i, real_column + 1] = char

with open("map.txt", 'w') as f:
    for r in warehouse:
        f.write("".join(r))
        f.write("\n")
moves = "".join([line.strip() for line in lines[SIZE + 1:]])

move_directions = {
    ">": [0, 1],
    "v": [1, 0],
    "<": [0, -1],
    "^": [-1, 0]
}
def find_next_level_objects(objects: list, direction: int):
    next_level_objects = set()
    for object in objects:
        if warehouse[object[0] + direction, object[1]] == "#":
            return ["#"]
        elif warehouse[object[0] + direction, object[1]] == "[":
            next_level_objects.add((object[0] + direction, object[1]))
            next_level_objects.add((object[0] + direction, object[1] + 1))
        elif warehouse[object[0] + direction, object[1]] == "]":
            next_level_objects.add((object[0] + direction, object[1]))
            next_level_objects.add((object[0] + direction, object[1] - 1))
    return list(next_level_objects)
    
    
def try_moving(row: int, column:int, move: str) -> Tuple[int, int]:
    direction = move_directions[move]
    next_row = row + direction[0]
    next_column = column + direction[1]
    if direction[0] == 0:
        while warehouse[next_row][next_column] in "[]":
            next_column += direction[1]
        if warehouse[next_row][next_column] == ".":
            while next_column != column:
                warehouse[next_row][next_column] = warehouse[next_row][next_column - direction[1]]
                next_column -= direction[1]
            warehouse[next_row][next_column] = "."
            return row + direction[0], column + direction[1]
        return row, column
    else:
        objects_to_move = [[(row, column)]]
        next_level_objects = find_next_level_objects([(row, column)], direction[0])
        while "#" not in next_level_objects and len(next_level_objects) > 0:
            objects_to_move.append(next_level_objects)
            next_level_objects = find_next_level_objects(next_level_objects, direction[0])
        if len(next_level_objects) == 0:
            for level in reversed(objects_to_move):
                for field in level:
                    warehouse[field[0] + direction[0], field[1]] = warehouse[field[0], field[1]]
                    warehouse[field[0], field[1]] = "."
            return row + direction[0], column
        return row, column
        
        
for move in moves:
    row, column = try_moving(row, column, move)


result = 0
it = np.nditer(warehouse, flags=['multi_index'])
for field in it:
    if field == "[":
        result += it.multi_index[0] * 100 + it.multi_index[1]
end = time()
print(result)
print(end - start)