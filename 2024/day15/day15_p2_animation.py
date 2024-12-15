from time import sleep
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.animation import FuncAnimation, FFMpegWriter
from typing import Tuple
SIZE = 50


with open("input.txt") as f:
    lines = f.readlines()
warehouse = np.zeros((SIZE, SIZE * 2), dtype=str)
for i, line in enumerate(lines[:SIZE]):
    for j, char in enumerate(line.strip()):
        real_column = 2 * j
        if char == "O":
            warehouse[i, real_column] = "["
            warehouse[i, real_column + 1] = "]"
        elif char == "@":
            row = i
            column = real_column
            warehouse[i, real_column] = "@"
            warehouse[i, real_column + 1] = "."
        else:
            warehouse[i, real_column] = char
            warehouse[i, real_column + 1] = char

moves = "".join([line.strip() for line in lines[SIZE + 1:]])

move_directions = {
    ">": [0, 1],
    "v": [1, 0],
    "<": [0, -1],
    "^": [-1, 0]
}
def find_next_level_objects(objects: list, direction: int):
    next_level_objects = set()
    for object in objects:
        if warehouse[object[0] + direction, object[1]] == "#":
            return ["#"]
        elif warehouse[object[0] + direction, object[1]] == "[":
            next_level_objects.add((object[0] + direction, object[1]))
            next_level_objects.add((object[0] + direction, object[1] + 1))
        elif warehouse[object[0] + direction, object[1]] == "]":
            next_level_objects.add((object[0] + direction, object[1]))
            next_level_objects.add((object[0] + direction, object[1] - 1))
    return list(next_level_objects)
    
    
def try_moving(row: int, column:int, move: str) -> Tuple[int, int]:
    direction = move_directions[move]
    next_row = row + direction[0]
    next_column = column + direction[1]
    if direction[0] == 0:
        while warehouse[next_row][next_column] in "[]":
            next_column += direction[1]
        if warehouse[next_row][next_column] == ".":
            while next_column != column:
                warehouse[next_row][next_column] = warehouse[next_row][next_column - direction[1]]
                next_column -= direction[1]
            warehouse[next_row][next_column] = "."
            return row, column + direction[1]
        return row, column
    else:
        objects_to_move = [[(row, column)]]
        next_level_objects = find_next_level_objects([(row, column)], direction[0])
        while "#" not in next_level_objects and len(next_level_objects) > 0:
            objects_to_move.append(next_level_objects)
            next_level_objects = find_next_level_objects(next_level_objects, direction[0])
        if len(next_level_objects) == 0:
            for level in reversed(objects_to_move):
                for field in level:
                    warehouse[field[0] + direction[0], field[1]] = warehouse[field[0], field[1]]
                    warehouse[field[0], field[1]] = "."
            return row + direction[0], column
        return row, column
        

# Set up the figure and colormap
color_groups = {
    "@": "red",
    ".": "blue",
    "#": "green",
    "[": "yellow",
    "]": "yellow"
}
numerical_data = np.vectorize(color_groups.get)(warehouse)

# Define a colormap with distinct colors
fig, ax = plt.subplots()

ax.axis("off")
for spine in ax.spines.values():
    spine.set_visible(False)  # Remove the plot's frame


def update_plot():
    ax.clear()  # Clear the current frame
    ax.set_xlim(0, warehouse.shape[1])
    ax.set_ylim(0, warehouse.shape[0])
    ax.set_xticks([])  # Hide x-axis ticks
    ax.set_yticks([])  # Hide y-axis ticks
    ax.set_xticklabels([])  # Hide x-axis labels
    ax.set_yticklabels([])  # Hide y-axis labels
    
    # Plot each symbol at the correct position with the corresponding color
    for row in range(warehouse.shape[0]):
        for col in range(warehouse.shape[1]):
            symbol = warehouse[row, col]
            color = color_groups.get(symbol, "black")  # Default to black if no color is mapped
            ax.text(col, warehouse.shape[0] - row - 1, symbol, ha="center", va="center", fontsize=15, color=color)



writer = FFMpegWriter(fps=5, metadata={"artist": "User"}, bitrate=1800)


# Save the animation
output_file = "warehouse_animation_mini.mp4"
with writer.saving(fig, output_file, dpi=100):
    # Add initial frame
    update_plot()
    writer.grab_frame()
    for move in moves:  # Example: 20 iterations
        # Simulate updating the warehouse (replace with your logic)
        row, column = try_moving(row, column, move)
        # Update the plot
        # Add the current frame to the animation
        update_plot()
        writer.grab_frame()
        
    # Loop to update the warehouse and add frames
result = 0
it = np.nditer(warehouse, flags=['multi_index'])
for field in it:
    if field == "[":
        result += it.multi_index[0] * 100 + it.multi_index[1]
print(result)
