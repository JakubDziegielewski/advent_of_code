import numpy as np
from time import time

class Node():
    def __init__(self, x:int, y:int, val:int):
        self.x = x
        self.y = y
        self.val = val
        self.neighbors = []
        self.reachable_nines = set([(self.x, self.y)]) if val == 9 else None
        self.connections_to_nine = 1 if val == 9 else None
        
    def __eq__(self, other):
        if type(other) != Node:
            return False
        return other.x == self.x and other.y == self.y
    
    def find_connections(self) -> None:
        self.reachable_nines = set()
        for neighbor in self.neighbors:
            if not neighbor.reachable_nines is None:
                self.reachable_nines = self.reachable_nines | neighbor.reachable_nines
            else:
                neighbor.find_connections()
                self.reachable_nines = self.reachable_nines | neighbor.reachable_nines
    def count_connections(self) -> None:
        self.connections_to_nine = 0
        for neighbor in self.neighbors:
            if not neighbor.connections_to_nine is None:
                self.connections_to_nine += neighbor.connections_to_nine
            else:
                neighbor.count_connections()
                self.connections_to_nine += neighbor.connections_to_nine

start = time()
with open("input.txt") as f:
    array = list(map(list, f.read().split("\n")))
nodes = np.zeros((len(array), len(array[0])), dtype=Node)
for i, row in enumerate(array):
    for j, column in enumerate(row):
        nodes[i, j] = Node(int(i), int(j), int(column))
        if i > 0:
            diff = nodes[i - 1, j].val - nodes[i, j].val
            if diff == 1:
                nodes[i, j].neighbors.append(nodes[i - 1, j])
            elif diff == -1:
                nodes[i - 1, j].neighbors.append(nodes[i, j])
        if j > 0:
            diff = nodes[i, j - 1].val - nodes[i, j].val
            if diff == 1:
                nodes[i, j].neighbors.append(nodes[i, j  -1])
            elif diff == -1:
                nodes[i, j - 1].neighbors.append(nodes[i, j])

result_one = 0
result_two = 0
for row in nodes:
    for node in row:
        if node.val == 0:
            node.find_connections()
            node.count_connections()
            result_one += len(node.reachable_nines)
            result_two += node.connections_to_nine

end = time()
print(result_one)
print(result_two)
print(f"Time: {end - start:.4f} seconds")
