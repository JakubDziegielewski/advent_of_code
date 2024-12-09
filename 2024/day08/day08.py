import re
from string import digits, ascii_uppercase, ascii_lowercase
from typing import Tuple
from time import time

start = time()
result = set()
nodes = digits + ascii_lowercase + ascii_uppercase
antinodes = {node:[] for node in nodes}
def check_if_antinode_exists(antinode: Tuple[int, int]) -> bool:
    return antinode[0] >= 0 and antinode[1] >= 0 and antinode[0] < 50 and antinode[1] < 50
def tuple_difference(tuple_one: Tuple[int, int], tuple_two: Tuple[int, int]):
    return tuple_one[0] - tuple_two[0], tuple_one[1] - tuple_two[1]
def tuple_sum(tuple_one: Tuple[int, int], tuple_two: Tuple[int, int]):
    return tuple_one[0] + tuple_two[0], tuple_one[1] + tuple_two[1]
with open("input.txt") as f:
    lines = f.readlines()
    for i, line in enumerate(lines):
        matches = re.finditer(r"[a-zA-Z0-9]", line)
        for m in matches:
            character = m.group()
            list_of_coords = antinodes[character]
            new_coords = (i, m.start())
            for coords in list_of_coords:
                diff = tuple_difference(new_coords, coords)
                first_antinode = tuple_difference(coords, diff)
                second_antinode = tuple_sum(new_coords, diff)
                if check_if_antinode_exists(first_antinode):
                    result.add(first_antinode)
                if check_if_antinode_exists(second_antinode):
                    result.add(second_antinode)
            antinodes[character].append(new_coords)
print(len(result))

result = set()
antinodes = {node:[] for node in nodes}
with open("input.txt") as f:
    lines = f.readlines()
    for i, line in enumerate(lines):
        matches = re.finditer(r"[a-zA-Z0-9]", line)
        for m in matches:
            character = m.group()
            list_of_coords = antinodes[character]
            new_coords = (i, m.start())
            for coords in list_of_coords:
                diff = tuple_difference(new_coords, coords)
                first_antinode = tuple_difference(coords, diff)
                second_antinode = tuple_sum(new_coords, diff)
                while check_if_antinode_exists(first_antinode):
                    result.add(first_antinode)
                    first_antinode = tuple_difference(first_antinode, diff)
                while check_if_antinode_exists(second_antinode):
                    result.add(second_antinode)
                    second_antinode = tuple_sum(second_antinode, diff)
            antinodes[character].append(new_coords)
            if len(antinodes[character]) > 2:
                result.add(antinodes[character][-1])
            elif len(antinodes[character]) > 1:
                result.add(antinodes[character][0])
                result.add(antinodes[character][1])
end = time()
print(len(result))

print(end - start)