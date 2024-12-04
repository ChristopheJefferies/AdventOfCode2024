filename = "input4.txt"
with open(filename) as file:
    input = [line.rstrip() for line in file]

import numpy as np
import itertools

# Part 1

# Preprocess input
input = [list(string) for string in input]
input = np.array(input)
grid_height, grid_width = input.shape

# Grid movement directions
directions = list(itertools.product([-1, 0, 1], [-1, 0, 1]))
directions.remove((0, 0))
directions = [
    np.array(direction) for direction in directions
]  # For ease of elementwise adding like vectors


def words_around(x: int, y: int, length: int) -> list[str]:
    """
    Return a list of all straight-line 'words' of the given length out from
    coordinate (x, y) which fit in the grid.
    """
    output = []

    for direction in directions:
        start = np.array([x, y])
        end = start + (length - 1) * direction

        if (0 <= end[0] < grid_height) and (0 <= end[1] < grid_width): # Word fits in the grid
            word_coords = [start + (i * direction) for i in range(length)]
            output.append(''.join(input[x][y] for [x, y] in word_coords))

    return output


output = 0

for row, col in itertools.product(range(grid_height), range(grid_width)):
    if input[row, col] == 'X':
        words = words_around(row, col, 4)
        output += words.count('XMAS')

print(output)


# Part 2

output2 = 0

centres = itertools.product(
    range(1, grid_height - 1), range(1, grid_width - 1)
)

for row, col in centres:
    if input[row][col] == 'A':
        corners = [
            input[row + 1][col + 1],
            input[row - 1][col - 1],
            input[row + 1][col - 1],
            input[row - 1][col + 1],
        ]

        if (set(corners) == {'M', 'S'}) and (corners[0] != corners[1]) and (corners[2] != corners[3]):
            output2 += 1
    
print(output2)