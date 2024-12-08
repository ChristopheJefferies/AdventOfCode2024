filename = "input8.txt"
with open(filename) as file:
    input = [line.rstrip() for line in file]

import numpy as np
from collections import defaultdict
from itertools import combinations

GRID_HEIGHT = len(input)
GRID_WIDTH = len(input[0])

# Find locations of antennae of each frequency
antennae = defaultdict(list)
for row, line in enumerate(input):
    for col, char in enumerate(line):
        if char != ".":
            antennae[char].append(np.array((row, col)))


def is_in_grid(coord):
    return (0 <= coord[0] < GRID_HEIGHT) and (0 <= coord[1] < GRID_WIDTH)


def find_antinodes(char: str) -> int:
    """
    Return the number of antinodes within the grid created by antennae with
    frequency char
    """
    antinodes = set()
    # Antennae are resonant antinodes (if there's at least 2 of them - handled at the end)
    antinodes2 = {tuple(antenna) for antenna in antennae[char]}

    # Part 1
    for antenna1, antenna2 in combinations(antennae[char], 2):
        antinode1 = 2 * antenna1 - antenna2  # Possible antinode on the antenna1 side
        if is_in_grid(antinode1):
            antinodes.add(tuple(antinode1))

        antinode2 = 2 * antenna2 - antenna1  # Possible antinode on the antenna1 side
        if is_in_grid(antinode2):
            antinodes.add(tuple(antinode2))

    # Part 2
    for antenna1, antenna2 in combinations(antennae[char], 2):
        step = antenna1 - antenna2  # Antinodes on the antenna1 side
        next_antinode = antenna1 + step
        while is_in_grid(next_antinode):
            antinodes2.add(tuple(next_antinode))  # Take tuple for hashing in to a set
            next_antinode += step

        step = antenna2 - antenna1  # Antinodes on the antenna2 side
        next_antinode = antenna2 + step
        while is_in_grid(next_antinode):
            antinodes2.add(tuple(next_antinode))
            next_antinode += step

    if len(antinodes2) == 1:  # A lone antenna doesn't create resonant antinodes
        antinodes2 = set()

    return antinodes, antinodes2


antinodes, antinodes2 = set(), set()
for char in antennae:
    non_resonant, resonant = find_antinodes(char)
    antinodes = antinodes.union(non_resonant)
    antinodes2 = antinodes2.union(resonant)
print(len(antinodes), len(antinodes2))
