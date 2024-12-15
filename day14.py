import math
import numpy as np

filename = "input14.txt"

# Grid size comes from problem specification, not the input
GRID_WIDTH = 101
GRID_HEIGHT = 103

# Parse input
input = []
with open(filename) as file:
    for line in file:
        pos, vel = line.split()
        px, py = pos[2:].split(",")
        vx, vy = vel[2:].split(",")
        input.append([int(px), int(py), int(vx), int(vy)])

# Part 1

# Number quadrants 0,1,2,3 in reading order
quadrant_counts = {i: 0 for i in range(4)}

vert_divide = (GRID_WIDTH - 1) // 2
hori_divide = (GRID_HEIGHT - 1) // 2


def increment_quadrant(x: int, y: int) -> None:
    """
    Find which quadrant (x, y) lies in (if any) and increment the relevant
    dictionary value.
    """
    if x < vert_divide:
        if y < hori_divide:
            quadrant_counts[0] += 1
        elif y > hori_divide:
            quadrant_counts[2] += 1

    elif x > vert_divide:
        if y < hori_divide:
            quadrant_counts[1] += 1
        elif y > hori_divide:
            quadrant_counts[3] += 1

    return


def final_position(robot: list[int], seconds=100) -> tuple[int]:
    """
    Return the final position of the robot with the given starting position and
    velocity after the given number of seconds.
    """
    px, py, vx, vy = robot
    final_x = (px + seconds * vx) % GRID_WIDTH
    final_y = (py + seconds * vy) % GRID_HEIGHT
    return final_x, final_y


for robot in input:
    increment_quadrant(*final_position(robot))

print(math.prod(quadrant_counts.values()))


# Part 2
# Need all the robots' positions at each step now rather than finding them one at a time.


class Robot:
    def __init__(self, robot_info):
        self.px, self.py, self.vx, self.vy = robot_info
        self.position = (self.px, self.py)

    def step(self):
        self.px = (self.px + self.vx) % GRID_WIDTH
        self.py = (self.py + self.vy) % GRID_HEIGHT


robots = [Robot(robot) for robot in input]

"""
From a look at the first few outputs, these seemed to have significant clustering (alternating tall/wide):
1, 48, 104, 149, 207, 250
A look at outputs with (frame % 103 == 1) or (frame % 101 == 48) revealed the answer quickly enough.
"""

for frame in range(7623):
    for robot in robots:
        robot.step()

grid = 0 * np.empty((GRID_HEIGHT, GRID_WIDTH), dtype=np.int8)
grid[[robot.py for robot in robots], [robot.px for robot in robots]] = (
    1  # The problem uses coords for cols then rows
)

with open("output14.txt", "w") as file:
    for line in grid:
        string = ["#" if i else " " for i in line]
        file.write("".join(string) + "\n")
