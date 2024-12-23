import networkx as nx
from time import time

s = time()
graph = nx.Graph()

with open("2024/day23/input.txt") as f:
    lines = f.readlines()
    
connections = [connection.strip().split("-") for connection in lines]
for connection in connections:
    computer_one = connection[0]
    computer_two = connection[1]
    if not graph.has_node(computer_one):
        graph.add_node(computer_one)
    if not graph.has_node(computer_two):
        graph.add_node(computer_two)
    graph.add_edge(computer_one, computer_two)
    
class NodeSet:
    def __init__(self, nodes):
        self.nodes = sorted(nodes)
    
    def __hash__(self):
        return hash("".join(self.nodes))

    def __eq__(self, value):
        return self.nodes == value.nodes
    
    def add_node(self, node):
        self.nodes.append(node)
        self.nodes.sort()

triangles = set()


for node in graph.nodes:
    neighbors = graph.neighbors(node)
    for neighbor in neighbors:
        second_neigbors = graph.neighbors(neighbor)
        for second_neighbor in second_neigbors:
            third_neighbors = graph.neighbors(second_neighbor)
            if node in third_neighbors:
                if "t" in [node[0], neighbor[0], second_neighbor[0]]:
                    triangle = NodeSet([node, neighbor, second_neighbor])
                    triangles.add(triangle)
print(len(triangles))

result = set()
for triangle in triangles:
    for node in list(graph.nodes):
        if node in triangle.nodes:
            continue
        neighbors = graph.neighbors(node)
        if set(triangle.nodes) <= set(neighbors):
            new_set = list(triangle.nodes)
            new_set.append(node)
            result.add(NodeSet(new_set))
            

for node in list(graph.nodes):
    for node_set in triangles:
        if node in node_set.nodes:
            continue
        neighbors = graph.neighbors(node)
        if set(node_set.nodes) <= set(neighbors):
            node_set.add_node(node)
max_len = 0
for node_set in triangles:
    if len(node_set.nodes) > max_len:
        max_len = len(node_set.nodes)
        result = node_set.nodes
print(",".join(result))
e = time()
print(e - s)

        
        