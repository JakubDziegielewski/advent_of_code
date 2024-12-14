import numpy as np
np.set_printoptions(suppress=True,linewidth=240)

WIDTH = 101
HEIGHT = 103
middle_x = WIDTH // 2
middle_y = HEIGHT // 2
final_list = [[0, 0], [0, 0]]
map_of_robots = np.array([[0] * WIDTH] * HEIGHT)

with open("input.txt") as f:
    lines = f.readlines()

class Robot:
    def __init__(self, x, y, velocity_x, velocity_y):
        self.x = x
        self.y = y
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
    def change_position(self):
        self.x = (self.x + self.velocity_x) % WIDTH
        self.y = (self.y + self.velocity_y) % HEIGHT
robots =np.zeros(len(lines), dtype=Robot)


for line in lines:
    array = line.split()
    starting_pos = array[0].split(",")
    velocity = array[1].split(",")
    starting_pos_x, starting_pos_y = int(starting_pos[0][2:]), int(starting_pos[1])
    velocity_x, velocity_y = int(velocity[0][2:]), int(velocity[1])
    position_x = (starting_pos_x + 100 * velocity_x) % WIDTH
    position_y = (starting_pos_y + 100 * velocity_y) % HEIGHT
    if position_x == middle_x or position_y == middle_y:
        continue
    left = int(position_x > middle_x)
    upper = int(position_y > middle_y)
    final_list[upper][left] += 1
result = final_list[0][0] * final_list[0][1] * final_list[1][0] * final_list[1][1]
print(result)
for i, line in enumerate(lines):
    array = line.split()
    starting_pos = array[0].split(",")
    velocity = array[1].split(",")
    starting_pos_x, starting_pos_y = int(starting_pos[0][2:]), int(starting_pos[1])
    velocity_x, velocity_y = int(velocity[0][2:]), int(velocity[1])
    map_of_robots[starting_pos_y][starting_pos_x] += 1
    robots[i] = Robot(starting_pos_x, starting_pos_y, velocity_x, velocity_y)

for a in map_of_robots:
    for b in a:
        if b == 0:
            print(" ", end = "")
        else:
            print("*", end= "")

s = 1
while True:
    map_of_robots = np.array([[0] * WIDTH] * HEIGHT)
    for r in robots:
        r.change_position()
        map_of_robots[r.y][r.x] += 1
    if any(sum(x) >= 20 for x in map_of_robots) and any(sum(y) >= 20 for y in map_of_robots.T):
        for a in map_of_robots:
            print()
            for b in a:
                if b == 0:
                    print(" ", end = "")
                else:
                    print("*", end= "")
        print(s)
        input()
    s += 1
