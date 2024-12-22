from collections import defaultdict
from copy import deepcopy
from heapq import heappop, heappush

KEYBOARD_ONE = [
    ["7", "8", "9"],
    ["4", "5", "6"],
    ["1", "2", "3"],
    ["#", "0", "A"],
]
KEYBOARD_TWO = [
    ["#", "^", "A"],
    ["<", "v", ">"]
]



class Node:
    def __init__(self, char):
        self.char = char
        self.visited = False
        self.reaching_weight = None
        self.directions = []
    def set_reaching_weight(self, weight):
        self.reaching_weight = weight
    def __lt__(self, other):
        return self.reaching_weight < other.reaching_weight
class Edge:
    def __init__(self, final_node, direction):
        self.final_node = final_node
        self.direction = direction
        self.weight = 1
    def __repr__(self):
        return f"Final Node: {self.final_node}, Direction: {self.direction}"
nodes_one = dict()
nodes_two = dict()
edges_one = defaultdict(list)
edges_two = defaultdict(list)
for i, row in enumerate(KEYBOARD_ONE):
    for j, key in enumerate(row):
        if key == "#":
            continue
        nodes_one[key] = Node(key)
        if i > 0 and KEYBOARD_ONE[i - 1][j] != "#":
            edges_one[key].append(Edge(KEYBOARD_ONE[i - 1][j], "^"))
            edges_one[KEYBOARD_ONE[i - 1][j]].append(Edge(key, "v"))
        if j > 0 and KEYBOARD_ONE[i][j - 1] != "#":
            edges_one[key].append(Edge(KEYBOARD_ONE[i][j - 1], "<"))
            edges_one[KEYBOARD_ONE[i][j - 1]].append(Edge(key, ">"))
for i, row in enumerate(KEYBOARD_TWO):
    for j, key in enumerate(row):
        if key == "#":
            continue
        nodes_two[key] = Node(key)
        if i > 0 and KEYBOARD_TWO[i - 1][j] != "#":
            edges_two[key].append(Edge(KEYBOARD_TWO[i - 1][j], "^"))
            edges_two[KEYBOARD_TWO[i - 1][j]].append(Edge(key, "v"))
        if j > 0 and KEYBOARD_TWO[i][j - 1] != "#":
            edges_two[key].append(Edge(KEYBOARD_TWO[i][j - 1], "<"))
            edges_two[KEYBOARD_TWO[i][j - 1]].append(Edge(key, ">"))

with open("2024/day21/input.txt") as f:
    lines = [x.strip() for x in f.readlines()]
found_paths_one = dict()
found_paths_two = dict()
result_strings_one = []
numbers = [int(x[:3]) for x in lines]

custom_order = {"v": 0, "<": 1, ">": 3, "^": 2}
def process_keyboard(result_strings_previous, used_nodes, used_edges, found_paths, verbose = False) -> list:
    result_strings = []
    for line in result_strings_previous:
        result_string = ""
        line = "A" + line
        for i in range(len(line) - 1):
            nodes = deepcopy(used_nodes)
            char = line[i]
            final_char = line[i + 1]
            if char == final_char:
                result_string += "A"
                continue
            if (char, final_char) in found_paths.keys():
                if verbose:
                    print(found_paths[(char, final_char)])
                result_string += "".join(found_paths[(char, final_char)])
                result_string += "A"
                continue
            open_list = []
            nodes[char].reaching_weight = 0
            heappush(open_list, nodes[char])
            while len(open_list) > 0:
                 node = heappop(open_list)
                 if node.char == final_char:
                    node.directions = sorted(node.directions, key=lambda x: custom_order[x])
                    if check_if_arms_go_out(char, node.directions):
                        node.directions = node.directions[::-1]
                    if verbose:
                        print(node.directions)
                    found_paths[(char, final_char)]= node.directions
                    result_string += "".join(node.directions)
                    result_string += "A"
                    break
                 edges = used_edges[node.char]
                 for edge in edges:
                     final_node = nodes[edge.final_node]
                     if final_node.reaching_weight is None:
                         final_node.set_reaching_weight(1 + node.reaching_weight)
                         final_node.directions = node.directions + [edge.direction]
                         heappush(open_list, final_node)
        result_strings.append(result_string)
    return result_strings
def check_if_arms_go_out(char, directions):
    if char == "A":
        return len(directions) > 1 and directions[:2] == ["<", "<"]
    elif char == "0":
        return directions[0] == "<"
    elif char == "1":
        return directions[0] == "v"
    elif char == "4":
        return len(directions) > 1 and directions[:2] == ["v", "v"]
    elif char == "7":
        return len(directions) > 2 and directions[:3] == ["v", "v", "v"]
    elif char == "<":
        return directions[0] == "^"
    elif char == "^":
        return directions[0] == "<"
def find_next_states(first_char, final_char, used_nodes, used_edges):
    if first_char == final_char:
        return "A"
    result_string = ""
    nodes = deepcopy(used_nodes)
    char = first_char
    open_list = []
    nodes[char].reaching_weight = 0
    heappush(open_list, nodes[char])
    while len(open_list) > 0:
         node = heappop(open_list)
         if node.char == final_char:
            node.directions = sorted(node.directions, key=lambda x: custom_order[x])
            if check_if_arms_go_out(char, node.directions):
                node.directions = node.directions[::-1]
            result_string += "".join(node.directions)
            result_string += "A"
            break
         edges = used_edges[node.char]
         for edge in edges:
             final_node = nodes[edge.final_node]
             if final_node.reaching_weight is None:
                 final_node.set_reaching_weight(1 + node.reaching_weight)
                 final_node.directions = node.directions + [edge.direction]
                 heappush(open_list, final_node)
    return result_string
chars = ["<", ">", "^", "v", "A"]

transforms = dict()
for char in chars:
    for c in chars:
        transforms[(char, c)] = find_next_states(char, c, nodes_two, edges_two)
        

res_one = process_keyboard(lines, nodes_one, edges_one, found_paths_one)
res_one = process_keyboard(res_one, nodes_two, edges_two, found_paths_two)
res_one = process_keyboard(res_one, nodes_two, edges_two, found_paths_two)

result = 0

for s, n in zip(res_one, numbers):
    result += len(s) * n
print(result)


