import numpy as np
from typing import Tuple
import re
import time


class Guard:
    def __init__(self, position: Tuple[int, int], horizontal_movement: int, vertical_movement: int):
        self.position = position
        self.horizontal_movement = horizontal_movement
        self.vertical_movement = vertical_movement
        self.visited_fields = 1
    def move(self, position: Tuple[int, int]) -> None:
        self.position = position
    def get_next_field(self) -> Tuple[int, int]:
        return self.position[0] + self.vertical_movement, self.position[1] + self.horizontal_movement
    def change_direction(self) -> None:
        temp = self.vertical_movement
        self.vertical_movement = self.horizontal_movement
        self.horizontal_movement = -temp
    def find_next_obstacle(self, guardian_map: np.ndarray) -> Tuple[int, int] | None:
        if self.vertical_movement == -1:
            path =  guardian_map[:self.position[0] + 1, [self.position[1]]][::-1]
            condition = np.where(path == "#")[0]
            if condition.size > 0:
                obstacle = condition[0]
                return self.position[0] - obstacle, self.position[1]
            else:
                return None
        elif self.vertical_movement == 1:
            path =  guardian_map[self.position[0]:, [self.position[1]]]
            condition = np.where(path == "#")[0]
            if condition.size > 0:
                obstacle = condition[0]
                return self.position[0] + obstacle, self.position[1]
            else:
                return None
        elif self.horizontal_movement == -1:
            path =  guardian_map[self.position[0]][:self.position[1] + 1][::-1]
            condition = np.where(path == "#")[0]
            if condition.size > 0:
                obstacle = condition[0]
                return self.position[0], self.position[1] - obstacle
            else:
                return None
        else:
            path =  guardian_map[self.position[0]][self.position[1]:]
            
            condition = np.where(path == "#")[0]
            if condition.size > 0:
                obstacle = condition[0]
                return self.position[0], self.position[1] + obstacle
            else:
                return None
        

with open("input.txt") as f:
    guardian_map = np.zeros((132, 132), dtype="str")
    txt = f.read()
    strings = txt.split("\n")
    for i, s in enumerate(strings):
        arrow = re.search("[\^\>v\<]", s)
        if arrow:
            group = arrow.group()
            position = (i, arrow.start())
        guardian_map[i] = np.array(list(s.strip()))
if group == "^":
    horizontal_movement = 0
    vertical_movement = -1
elif group == ">":
    horizontal_movement = 1
    vertical_movement = 0
elif group == "v":
    horizontal_movement = 0
    vertical_movement = 1
else:
    horizontal_movement = -1
    vertical_movement = 0
    
guard = Guard(position, horizontal_movement, vertical_movement)

start = time.time()
guardian_map[position] = "X"
next_field = guard.get_next_field()
next_symbol = guardian_map[next_field]
while next_symbol != "*":
    if next_symbol == ".":
        guard.move(next_field)
        guardian_map[next_field] = "X"
        guard.visited_fields += 1
    elif next_symbol == "#":
        guard.change_direction()
    else:
        guard.move(next_field)
    next_field = guard.get_next_field()
    next_symbol = guardian_map[next_field]
print(guard.visited_fields)
end = time.time()
print(end - start)


with open("input.txt") as f:
    guardian_map = np.zeros((132, 132), dtype="str")
    txt = f.read()
    strings = txt.split("\n")
    for i, s in enumerate(strings):
        arrow = re.search("[\^\>v\<]", s)
        if arrow:
            group = arrow.group()
            position = (i, arrow.start())
        guardian_map[i] = np.array(list(s.strip()))
guard.move(position)
guard.vertical_movement = vertical_movement
guard.horizontal_movement = horizontal_movement
next_field = guard.get_next_field()
succesful = set()
start = time.time()
while (next_symbol := guardian_map[next_field]) != "*":
    visited_obstructions = set()
    current_direction = (guard.horizontal_movement, guard.vertical_movement)
    if next_symbol == ".":
        guardian_map[next_field] = "#"
        while (next_obstacle := guard.find_next_obstacle(guardian_map)) is not None:
            if (next_obstacle, (guard.horizontal_movement, guard.vertical_movement)) in visited_obstructions:
                succesful.add(next_field)
                break
            else:
                visited_obstructions.add((next_obstacle, (guard.horizontal_movement, guard.vertical_movement)))
                guard.move((next_obstacle[0] - guard.vertical_movement, next_obstacle[1] - guard.horizontal_movement))
                guard.change_direction()
        guardian_map[next_field] = "X"
        guard.move(next_field)
        guard.horizontal_movement, guard.vertical_movement = current_direction
    elif next_symbol == "#":
        guard.change_direction()
    else:
        guard.move(next_field)
    next_field = guard.get_next_field()
print(len(succesful))
end = time.time()
print(end - start)