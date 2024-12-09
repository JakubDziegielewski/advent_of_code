rules = {k: set() for k in range(11, 100)}

with open("input.txt") as f:
    line = ""
    while (line := f.readline()) != "\n":
        lst = list(map(int, line.strip().split("|")))
        key, val = lst[0], lst[1]
        rules[key].add(val)
    updates = f.readlines()
 
result = 0   
for update in updates:
    update_lst = list(map(int, update.split(",")))
    for i, key in enumerate(update_lst):
        following_values = set(update_lst[i + 1:])
        if not following_values <= rules[key]:
            break
    else:
        result += update_lst[i // 2]
                
print(result)
    
result = 0
    
for update in updates:
    update_lst = list(map(int, update.split(",")))
    full_set = set(update_lst)
    full_set_size = len(full_set)
    mistake_caught = False
    middle_value = 0
    for i, key in enumerate(update_lst):
        difference = full_set - rules[key]
        difference_size = len(difference)
        if i != difference_size - 1:
            mistake_caught = True
            if middle_value != 0:
                result += middle_value
                break
        if difference_size - 1 == full_set_size // 2:
            middle_value = key
            if mistake_caught:
                result += middle_value
                break
print(result)

        
    