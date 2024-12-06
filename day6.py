filename = "input6.txt"
with open(filename) as file:
    input = [line.rstrip() for line in file]

import numpy as np
from collections import defaultdict

input = np.array([list(line) for line in input])
GRID_HEIGHT = len(input)
GRID_WIDTH = len(input[0])

directions = {
    "^": np.array([-1, 0]),
    ">": np.array([0, 1]),
    "v": np.array([1, 0]),
    "<": np.array([0, -1]),
}

next_directions = {"^": ">", ">": "v", "v": "<", "<": "^"}

# Part 1

# Find guard start location and direction
for char in directions:
    guard_coord = np.argwhere(input == char)[0]
    if guard_coord.size:
        guard_dir = char
        break

# Store these separately for part 2
guard_start = guard_coord
guard_dir_start = guard_dir


# Helper functions
def is_in_grid(coord):
    return (0 <= coord[0] < GRID_HEIGHT) and (0 <= coord[1] < GRID_WIDTH)


def next_coord(coord, direction):
    return coord + directions[direction]


def next_guard_coord():
    return next_coord(guard_coord, guard_dir)


# Trace path
path = {tuple(guard_coord)}  # Take a tuple (hashable) to form a set

while is_in_grid(next_guard_coord()):

    while input[*next_guard_coord()] == "#":  # Need to turn right
        guard_dir = next_directions[guard_dir]

    guard_coord = next_guard_coord()
    path.add(tuple(guard_coord))


print(len(path))  # Part 1 answer


# Part 2
# This is horribly slow but I don't have time to rewrite/optimise it :)

def obstacle_causes_loop(obstacle_coord: tuple) -> bool:
    """
    Return True if placing an obstacle there causes the guard to enter a loop,
    else False (if it exits the grid).
    """

    guard_coord, guard_dir = guard_start, guard_dir_start
    previous_states = defaultdict(set)  # Keys are direction strings, values are lists of coords where guard has been facing that way
    previous_states[guard_dir].add(tuple(guard_coord))

    while is_in_grid(next_coord(guard_coord, guard_dir)):
        
        while (
            input[*next_coord(guard_coord, guard_dir)] == "#"
            or tuple(next_coord(guard_coord, guard_dir)) == obstacle_coord
        ):  # Need to turn right
            guard_dir = next_directions[guard_dir]

        guard_coord = next_coord(guard_coord, guard_dir)
        
        if tuple(guard_coord) in previous_states[guard_dir]:  # Loop found
            return True
        previous_states[guard_dir].add(tuple(guard_coord))
    
    return False


# Only need to consider placing obstacles on the path from part 1.
# Can't take a set of coords (they're unhashable) so loop to find unique ones.
possible_obstacles = []
for coord in path:
    if not (coord in possible_obstacles):
        possible_obstacles.append(coord)
possible_obstacles.pop(0)  # Don't place an obstacle on the guard's starting location

output = 0
num_obstacles = len(possible_obstacles)
for i, obstacle in enumerate(possible_obstacles):
    if i % 100 == 0:
        print(f"{i}/{num_obstacles}")
    if obstacle_causes_loop(obstacle):
        output += 1

print(output)