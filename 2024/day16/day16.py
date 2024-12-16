import numpy as np
from typing import Tuple
from heapq import heappop, heappush
from time import time

#Directions: East -> 0, South -> 1, West -> 2, North -> 3


class Node:
    def __init__(self, heuristic_value:int):
        self.visited = False
        self.reaching_value = None
        self.heuristic_value = heuristic_value
        self.edges = []
        self.parents = set()
        self.added_to_parents = False

    def __lt__(self, other) -> bool:
        return self.reaching_value + self.heuristic_value < other.reaching_value + other.heuristic_value
    def __gt__(self, other) -> bool:
        return self.reaching_value + self.heuristic_value > other.reaching_value + other.heuristic_value
    
    def add_edge(self, x:int, y:int, direction: int, weight: int) -> None:
        self.edges.append((x, y, direction, weight))
    
edges = dict() #k -> starting node, v -> edge


s = time()
with open("input.txt") as f:
    lines = f.readlines()
    array = np.array([list(line.strip()) for line in lines])
    start = np.argwhere(array == "S")[0]
    end = np.argwhere(array == "E")[0]
    graph = np.zeros((len(lines), len(lines), 4), dtype = Node)
def add_four_nodes(row: int, column: int):
    row_tax = 1000 if row != end[0] else 0
    column_tax = 1000 if column != end[1] else 0
    distance = row - end[0] + end[1] - column
    graph[row, column, 0] = Node(distance + row_tax)
    graph[row, column, 1] = Node(distance + row_tax + column_tax)
    graph[row, column, 2] = Node(distance + row_tax + column_tax)
    graph[row, column, 3] = Node(distance + column_tax)
    for i in range(4):
        graph[row, column, i].add_edge(row, column, (i + 1) % 4, 1000)
        graph[row, column, i].add_edge(row, column, (i - 1) % 4, 1000)
def add_edges_with_node_above(row:int, column:int) -> None:
    graph[row, column, 3].add_edge(row - 1, column, 3, 1)
    graph[row - 1, column, 1].add_edge(row, column, 1, 1)

def add_edges_with_node_next(row:int, column:int) -> None:
    graph[row, column, 2].add_edge(row, column - 1, 2, 1)
    graph[row, column - 1, 0].add_edge(row, column, 0, 1)
    
for i, row in enumerate(array):
    row_tax = 1000 if i != end[0] else 0
    for j, char in enumerate(row):
        column_tax = 1000 if j != end[1] else 0
        if char != "#":
            add_four_nodes(i, j)
            if array[i - 1, j] != "#":
                add_edges_with_node_above(i, j)
            if array[i, j - 1] != "#":
                add_edges_with_node_next(i, j)

results = []
graph[start[0], start[1], 0].reaching_value = 0
open_list = [graph[start[0], start[1], 0]]

def add_parents(edge):
    if edge[3] == 1000:
        if graph[edge[0], edge[1], (edge[2] - 1) % 4].reaching_value is None:
            graph[edge[0], edge[1], edge[2]].parents.add((edge[0], edge[1], (edge[2] + 1) % 4))
        elif graph[edge[0], edge[1], (edge[2] + 1) % 4].reaching_value is None:
            graph[edge[0], edge[1], edge[2]].parents.add((edge[0], edge[1], (edge[2] - 1) % 4))
        elif graph[edge[0], edge[1], (edge[2] - 1) % 4].reaching_value < graph[edge[0], edge[1], (edge[2] + 1) % 4].reaching_value:
            graph[edge[0], edge[1], edge[2]].parents.add((edge[0], edge[1], (edge[2] - 1) % 4))
        elif graph[edge[0], edge[1], (edge[2] - 1) % 4].reaching_value > graph[edge[0], edge[1], (edge[2] + 1) % 4].reaching_value:
            graph[edge[0], edge[1], edge[2]].parents.add((edge[0], edge[1], (edge[2] + 1) % 4))
        else:
            graph[edge[0], edge[1], edge[2]].parents.add((edge[0], edge[1], (edge[2] - 1) % 4))
            graph[edge[0], edge[1], edge[2]].parents.add((edge[0], edge[1], (edge[2] + 1) % 4))
            
    elif edge[2] == 0:
        graph[edge[0], edge[1], edge[2]].parents.add((edge[0], edge[1] - 1, edge[2]))
    elif edge[2] == 1:
        graph[edge[0], edge[1], edge[2]].parents.add((edge[0] - 1, edge[1], edge[2]))
    elif edge[2] == 2:
        graph[edge[0], edge[1], edge[2]].parents.add((edge[0], edge[1] + 1, edge[2]))
    elif edge[2] == 3:
        graph[edge[0], edge[1], edge[2]].parents.add((edge[0] + 1, edge[1], edge[2]))

while len(open_list) > 0:
    current_node = heappop(open_list)
    current_node.visited = True
    if current_node.heuristic_value == 0:
        results.append(current_node.reaching_value)
    for edge in current_node.edges:
        if graph[edge[0], edge[1], edge[2]].visited:
            if edge[3] + current_node.reaching_value == graph[edge[0], edge[1], edge[2]].reaching_value:
                add_parents(edge)
            continue
        new_raching_value = edge[3] + current_node.reaching_value
        if graph[edge[0], edge[1], edge[2]].reaching_value is None:
            graph[edge[0], edge[1], edge[2]].reaching_value = new_raching_value
            add_parents(edge)
            heappush(open_list, graph[edge[0], edge[1], edge[2]])
        elif graph[edge[0], edge[1], edge[2]].reaching_value > new_raching_value:
            graph[edge[0], edge[1], edge[2]].reaching_value = new_raching_value
            graph[edge[0], edge[1], edge[2]].parents = set()
            add_parents(edge)
        elif graph[edge[0], edge[1], edge[2]].reaching_value == new_raching_value:
            add_parents(edge)

    

def create_parent_set(starting_node, parent_set):
    if starting_node.added_to_parents:
        return
    starting_node.added_to_parents = True
    for parent in starting_node.parents:
        parent_set.add((parent[0], parent[1]))
        next_node = graph[parent[0], parent[1], parent[2]]
        create_parent_set(next_node, parent_set)

final_set = set()
final_set.add((end[0], end[1]))
if graph[end[0], end[1], 0].reaching_value == graph[end[0], end[1], 3].reaching_value:
    create_parent_set(graph[end[0], end[1], 0], final_set)
    create_parent_set(graph[end[0], end[1], 3], final_set)
elif graph[end[0], end[1], 3].reaching_value is None or graph[end[0], end[1], 0].reaching_value < graph[end[0], end[1], 3].reaching_value:
    create_parent_set(graph[end[0], end[1], 0], final_set)
else:
    create_parent_set(graph[end[0], end[1], 3], final_set)
e = time()
print(results[0])
print(len(final_set))
print(e - s)


