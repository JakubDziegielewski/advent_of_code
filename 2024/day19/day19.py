from collections import defaultdict

with open("2024/day19/input.txt") as f:
    arr = f.read().split("\n\n")
    patterns = arr[0].split(", ")
    designs = arr[1].split("\n")
    
def check_if_possible(design, possible, impossible):
    if design in impossible:
        return False
    if design in possible:
        return True
    for pattern in patterns:
        design_len = len(design)
        pattern_len = len(pattern)
        if design_len > pattern_len:
            if design[design_len - pattern_len:] == pattern:
                if check_if_possible(design[:design_len - pattern_len], possible, impossible):
                    possible.add(design)
                    return True
        elif design == pattern:
            possible.add(design)
            return True
    impossible.add(design)
    return False
impossible = set()
possible = set()
result = 0
for design in designs:
    if check_if_possible(design, possible, impossible):
        result += 1
print(result)

result = 0
impossible = set()
possible = dict()
def count_possibilities(design, possible, impossible):
    possibilities = 0
    if design in impossible:
        return 0
    if design in possible.keys():
        return possible[design]
    for pattern in patterns:
        design_len = len(design)
        pattern_len = len(pattern)
        if design_len > pattern_len:
            if design[design_len - pattern_len:] == pattern:
                possibilities += count_possibilities(design[:design_len - pattern_len], possible, impossible)   
        elif design == pattern:
            possibilities += 1
    if possibilities > 0:
        possible[design] = possibilities
    else:
        impossible.add(design)
    return possibilities

impossible = set()
possible = defaultdict(int)
result = 0
for design in designs:
    result += count_possibilities(design, possible, impossible)
print(result)
