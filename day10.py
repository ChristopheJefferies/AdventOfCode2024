filename = "input10.txt"
with open(filename) as file:
    input = [line.rstrip() for line in file]

input = [[int(i) for i in line] for line in input]

MAX_ROW = len(input) - 1
MAX_COL = len(input[0]) - 1


def cells_around(row: int, col: int) -> list[tuple[int]]:
    """
    Return all the coordinates orthogonally touching the given one which are
    inside the grid
    """
    output = []
    if row > 0:
        output.append((row - 1, col))
    if row < MAX_ROW:
        output.append((row + 1, col))
    if col > 0:
        output.append((row, col - 1))
    if col < MAX_COL:
        output.append((row, col + 1))

    return output


def find_trails(row: int, col: int):
    """
    Return the coordinates of all 9s reachable by trails from the given
    coordinate, and the number of ways to reach them
    """

    height = input[row][col]
    if height == 9:
        return {(row, col)}, 1

    output, output2 = set(), 0
    for adj_row, adj_col in cells_around(row, col):
        if input[adj_row][adj_col] == height + 1:
            nines, num_trails = find_trails(adj_row, adj_col)
            output |= nines
            output2 += num_trails

    return output, output2


output = 0
output2 = 0
for row in range(MAX_ROW + 1):
    for col in range(MAX_COL + 1):
        if input[row][col] == 0:
            nines, num_trails = find_trails(row, col)
            output += len(nines)
            output2 += num_trails

print(output, output2)
