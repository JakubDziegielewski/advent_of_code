import numpy as np
with open("2024/day18/input.txt") as f:
    lines = f.readlines()
SIZE = 70
class Node:
    def __init__(self):
        self.union_id = None
    def set_union_id(self, id):
        self.union_id = id

class Union:
    def __init__(self, id, point):
        self.id = id
        self.highest = point[0]
        self.lowest = point[0]
        self.left = point[1]
        self.right = point[1]
        self.nodes = []
    def merge(self, other):
        self.highest = min(self.highest, other.highest)
        self.lowest = max(self.lowest, other.lowest)
        self.left = min(self.left, other.left)
        self.right = max(self.right, other.right)
        for node in other.nodes:
            graph[node[0], node[1]].set_union_id(self.id)
        self.nodes += other.nodes
       
            
graph = np.zeros((SIZE + 1, SIZE + 1), dtype=Node)
for i, row in enumerate(graph):
    for j, element in enumerate(row):
        graph[i, j] = Node()

unions = dict()
result = 0
id_counter = 0
for line in lines:
    array = line.split(",")
    column, row = int(array[0]), int(array[1])
    if graph[row, column].union_id is not None:
        continue
    graph[row, column].set_union_id(id_counter)
    unions[id_counter] = Union(id_counter, (row, column))
    unions[id_counter].nodes.append((row, column))
    id_counter += 1
    
    if row > 0:
        if not graph[row - 1, column].union_id is None and graph[row - 1, column].union_id != graph[row, column].union_id:
            unions[graph[row - 1, column].union_id].merge(unions[graph[row, column].union_id])
    if row < SIZE:
        if not graph[row + 1, column].union_id is None and graph[row + 1, column].union_id != graph[row, column].union_id:
            unions[graph[row + 1, column].union_id].merge(unions[graph[row, column].union_id])
    if column > 0:
        if not graph[row, column - 1].union_id is None and graph[row, column - 1].union_id != graph[row, column].union_id:
            unions[graph[row, column - 1].union_id].merge(unions[graph[row, column].union_id])
    if column < SIZE:
        if not graph[row, column + 1].union_id is None and graph[row, column + 1].union_id != graph[row, column].union_id:
            unions[graph[row, column + 1].union_id].merge(unions[graph[row, column].union_id])
    if row > 0 and column > 0:
        if not graph[row - 1, column - 1].union_id is None and graph[row - 1, column - 1].union_id != graph[row, column].union_id:
            unions[graph[row - 1, column - 1].union_id].merge(unions[graph[row, column].union_id])
    if row > 0 and column < SIZE:
        if not graph[row - 1, column + 1].union_id is None and graph[row - 1, column + 1].union_id != graph[row, column].union_id:
            unions[graph[row - 1, column + 1].union_id].merge(unions[graph[row, column].union_id])
    if row < SIZE and column > 0:
        if not graph[row + 1, column - 1].union_id is None and graph[row + 1, column - 1].union_id != graph[row, column].union_id:
            unions[graph[row + 1, column - 1].union_id].merge(unions[graph[row, column].union_id])
    if row < SIZE and column < SIZE:
        if not graph[row + 1, column + 1].union_id is None and graph[row + 1, column + 1].union_id != graph[row, column].union_id:
            unions[graph[row + 1, column + 1].union_id].merge(unions[graph[row, column].union_id])
    
    final_union = unions[graph[row, column].union_id]
    if final_union.highest == 0 and final_union.lowest == SIZE:
        print(f"{column},{row}")
        break
    elif final_union.left == 0 and final_union.right == SIZE:
        print(f"{column},{row}")
        break
    elif final_union.left == 0 and final_union.highest == 0:
        print(f"{column},{row}")
        break
    elif final_union.lowest == SIZE and final_union.right == SIZE:
        print(f"{column},{row}")
        break


