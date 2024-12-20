import numpy as np
from typing import Tuple
from time import time
class Node:
    def __init__(self):
        self.reaching_value = None
        self.edges = []
        self.next_index = None
    def add_edge(self, edge):
        self.edges.append(edge)
with open("2024/day20/input.txt") as f:
    lines = f.readlines()

s = time()
array = np.array([list(line.strip()) for line in lines])
start = np.argwhere(array == "S")[0]
start = start[0], start[1]
end = np.argwhere(array == "E")[0]
end = end[0], end[1]
graph = np.zeros(array.shape, dtype = Node)

it = np.nditer(array, flags=['multi_index'])
for _ in it:
    if array[it.multi_index] == "#":
        continue
    graph[it.multi_index] = Node()
    if array[it.multi_index[0] - 1, it.multi_index[1]] != "#":
        graph[it.multi_index[0] - 1, it.multi_index[1]].add_edge(it.multi_index)
        graph[it.multi_index].add_edge((it.multi_index[0] - 1, it.multi_index[1]))
    if array[it.multi_index[0], it.multi_index[1] - 1] != "#":
        graph[it.multi_index[0], it.multi_index[1] - 1].add_edge(it.multi_index)
        graph[it.multi_index].add_edge((it.multi_index[0], it.multi_index[1] - 1))

index = start
graph[start].reaching_value = 0
while index != end:
    next_index = graph[index].edges[0]
    if not graph[next_index].reaching_value is None:
        next_index = graph[index].edges[1]
    graph[next_index].reaching_value = graph[index].reaching_value + 1
    graph[index].next_index = next_index
    index = next_index


def check_condition(saved_time: int, distance: int = 2) -> bool:
    return saved_time - distance >= 100

def find_cheats_for_index(index: Tuple[int, int], max_distance: int) -> int:
    result = 0
    row, column = index
    start_row = max(row - max_distance, 1)
    final_row = min(array.shape[0] - 2, row + max_distance)
    start_column = max(column - max_distance, 1)
    final_column = min(array.shape[1] - 2, column + max_distance)
    for current_row in range(start_row, final_row + 1):
        distance = abs(row - current_row)
        if array[current_row, column] != "#":
            saved_time = graph[current_row, column].reaching_value - graph[row, column].reaching_value
            if check_condition(saved_time, distance):
                result += 1
        for i in range(1, max_distance - distance + 1):
            if column + i <= final_column:
                if array[current_row, column + i] != "#":
                    saved_time = graph[current_row, column + i].reaching_value - graph[row, column].reaching_value
                    if check_condition(saved_time, distance + i):
                        result += 1
            if column - i >= start_column:
                if array[current_row, column - i] != "#":
                    saved_time = graph[current_row, column - i].reaching_value - graph[row, column].reaching_value
                    if check_condition(saved_time, distance + i):
                        result += 1
    return result

index = start

p1, p2 = 0, 0
while index != end:
    p1 += find_cheats_for_index(index, 2)
    p2 += find_cheats_for_index(index, 20)
    index = graph[index].next_index
e = time()
print(p1)
print(p2)
print(e - s)
