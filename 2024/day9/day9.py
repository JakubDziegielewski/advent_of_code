from heapq import heappush, heappop
from time import time
start = time()
with open("input.txt") as f:
    string = f.readline()
    disk_map = list(map(int, string))


disk_size = sum(disk_map)
blocks = [0] * disk_size
curr_len = 0
files_size = 0
for i, length in enumerate(disk_map):
    if i % 2 == 0:
        blocks[curr_len:curr_len+length] = [i // 2] * length
        files_size += length
    curr_len += length


map_start_index = 1
blocks_start_index = disk_map[0]
map_end_index = len(disk_map) - 1
blocks_end_index = len(blocks) - 1
free_blocks = disk_map[map_start_index]
blocks_to_allocate = disk_map[map_end_index]
while blocks_start_index < blocks_end_index:
    if free_blocks > blocks_to_allocate:
        blocks[blocks_start_index:blocks_start_index + blocks_to_allocate] = blocks[blocks_end_index - blocks_to_allocate + 1:blocks_end_index+1]
        blocks_start_index += blocks_to_allocate
        blocks_end_index -= (blocks_to_allocate + disk_map[map_end_index - 1])
        map_end_index -= 2
        free_blocks -= blocks_to_allocate
        blocks_to_allocate = disk_map[map_end_index]  
    else:
        blocks[blocks_start_index:blocks_start_index + free_blocks] = blocks[blocks_end_index - free_blocks + 1:blocks_end_index+1]
        blocks_start_index += free_blocks + disk_map[map_start_index + 1]
        blocks_end_index -=  free_blocks
        map_start_index += 2
        blocks_to_allocate -= free_blocks
        free_blocks = disk_map[map_start_index]
result = 0

for i, id in enumerate(blocks[:files_size]):
    result += i * id
print(result)

blocks = [0] * disk_size
curr_len = 0
files_size = 0

free_space_lists = [[] for _ in range(10)]
def check_if_ended(end_index):
    for free_space_list in free_space_lists[1:]:
        if len(free_space_list) > 0 and free_space_list[0] < end_index:
            return False
    return True

def find_smallest_index(blocks_to_allocate, end_index):
    smallest_index = end_index
    space_size = None
    for i, free_space_list in enumerate(free_space_lists[blocks_to_allocate:]):
        if free_space_list:
            if free_space_list[0] < smallest_index:
                smallest_index = free_space_list[0]
                space_size = i + blocks_to_allocate
            elif free_space_list[0] > end_index:
                free_space_list = []
            
    return smallest_index, space_size

for i, length in enumerate(disk_map):
    if i % 2 == 0:
        blocks[curr_len:curr_len+length] = [i // 2] * length
        files_size += length
    else:
        heappush(free_space_lists[length], curr_len)
    curr_len += length


map_end_index = len(disk_map) - 1
blocks_end_index = len(blocks) - 1

while not check_if_ended(blocks_end_index):
    blocks_to_allocate = disk_map[map_end_index]
    index, space_size = find_smallest_index(blocks_to_allocate, blocks_end_index)
    if space_size != None:
        blocks[index:index+blocks_to_allocate] = blocks[blocks_end_index - blocks_to_allocate + 1:blocks_end_index+1]
        heappop(free_space_lists[space_size])
        new_size = space_size - blocks_to_allocate
        new_index = index + blocks_to_allocate
        heappush(free_space_lists[new_size], new_index)
        blocks[blocks_end_index - blocks_to_allocate + 1:blocks_end_index+1] = [0] * blocks_to_allocate
    blocks_end_index -= (blocks_to_allocate + disk_map[map_end_index - 1])
    map_end_index -= 2

result = 0
for i, id in enumerate(blocks):
    result += i * id
end = time()
print(result)

print(end - start)
