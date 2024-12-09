import numpy as np

input_array = np.loadtxt("input.txt", dtype=int).T
first = np.sort(input_array[0])
second = np.sort(input_array[1])

print(sum(abs(first - second)))

index = 0
score = 0
number_of_occurences = 0
last_number = 0
score_to_add = 0
max_index = len(second)
for number in first:
    if number == last_number:
        score += score_to_add
        continue
    while index < max_index and number > second[index]:
        index += 1
    number_of_occurences = 0
    score_to_add = 0
    while index < max_index and number == second[index]:
        number_of_occurences += 1
        index += 1
    score_to_add = number * number_of_occurences
    score += score_to_add
    last_number = number
print(score)
        
    
