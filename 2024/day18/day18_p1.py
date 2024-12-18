from heapq import heappop, heappush
import numpy as np
with open("input.txt") as f:
    lines = f.readlines()
class Node:
    def __init__(self, heuristic_value:int):
        self.visited = False
        self.reaching_value = None
        self.heuristic_value = heuristic_value
        self.edges = []

    def __lt__(self, other) -> bool:
        return self.reaching_value + self.heuristic_value < other.reaching_value + other.heuristic_value
    def __gt__(self, other) -> bool:
        return self.reaching_value + self.heuristic_value > other.reaching_value + other.heuristic_value
    
    def add_edge(self, x:int, y:int, weight: int) -> None:
        self.edges.append((x, y, weight))

graph = np.zeros((71, 71), dtype=Node)
grid = np.ones((71, 71), dtype=bool)

for line in lines[:1024]:
    array = line.split(",")
    x, y = int(array[0]), int(array[1])
    grid[x, y] = False
for i, row in enumerate(graph):
    for j, sign in enumerate(row):
        if grid[i, j]:
            graph[i, j] = Node(140 - i - j)
        else:
            continue
        if i > 0:
            if grid[i - 1, j]:
                graph[i, j].add_edge(i - 1, j, 1)
                graph[i - 1, j].add_edge(i, j, 1)
        if j > 0:
            if grid[i, j - 1]:
                graph[i, j].add_edge(i, j - 1, 1)
                graph[i, j - 1].add_edge(i, j, 1)

graph[0, 0].reaching_value = 0
open_list = [graph[0, 0]]
while len(open_list) > 0:
    current_node = heappop(open_list)
    current_node.visited = True
    if current_node.heuristic_value == 0:
        result = current_node.reaching_value
        break
    for edge in current_node.edges:
        new_raching_value = edge[2] + current_node.reaching_value
        if graph[edge[0], edge[1]].reaching_value is None:
            graph[edge[0], edge[1]].reaching_value = new_raching_value
            heappush(open_list, graph[edge[0], edge[1]])
        elif graph[edge[0], edge[1]].reaching_value > new_raching_value:
            graph[edge[0], edge[1]].reaching_value = new_raching_value
print(result)
