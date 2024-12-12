from collections import defaultdict



with open("input.txt") as f:
    array = list(f.read().split())
stones = defaultdict(int)
for a in array:
    stones[int(a)] += 1

def blink():
    stones_temp = dict(stones)
    for key, count in stones_temp.items():
        if stones[key] == 0:
            continue
        elif key == 0:
            stones[1] += count
            stones[0] -= count
        elif len(str(key)) % 2 == 0:
            str_key = str(key)
            half = len(str_key) // 2
            first = int(str_key[:half])
            second = int(str_key[half:])
            stones[first] += count
            stones[second] += count
            stones[key] -= count
        else:
            stones[key * 2024] += count
            stones[key] -= count

for i in range(25):
    blink()
print(sum(stones.values()))

for i in range(50):
    blink()
print(sum(stones.values()))