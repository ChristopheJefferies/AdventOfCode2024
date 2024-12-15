filename = "input15.txt"


# Util
def get_next_coord(coord: list[int], direction: str) -> tuple[int]:
    """
    Return the coord after moving one step in the given direction
    """
    row, col = coord

    if direction == "^":
        row -= 1
    elif direction == "v":
        row += 1
    elif direction == "<":
        col -= 1
    elif direction == ">":
        col += 1

    return [row, col]


class PartOne:
    def __init__(self, filename) -> None:
        self.filename = filename
        self.grid = []
        self.movements = ""
        self.robot_coord = [-1, -1]

    def parse_input(self) -> None:
        with open(self.filename) as f:
            input = [line.rstrip() for line in f]

        split = input.index("")  # Blank line between grid and movements
        self.grid = [list(line) for line in input[:split]]
        self.movements = "".join(input[split + 1 :])

    def find_robot(self) -> None:
        for i, row in enumerate(self.grid):
            if "@" in row:
                self.robot_coord = [i, row.index("@")]
                return

    def push(self, coord: list[int], direction: str) -> bool:
        """
        Push the object at position (x, y) in the grid in the given direction if possible.
        Do this by first pushing any other objects out of the way.
        Return True if it was possible, else False.
        """
        row, col = coord
        char = self.grid[row][col]

        if char == "#":  # Wall
            return False

        if char == ".":  # Free space
            return True

        # No check for exiting grid needed due to wall border
        next_coord = get_next_coord(coord, direction)

        # Deal with the object in front
        if not self.push(next_coord, direction):
            return False

        # Move this object
        self.grid[next_coord[0]][next_coord[1]] = char
        self.grid[row][col] = "."

        # Update robot position if it moved
        if char == "@":
            self.robot_coord = next_coord

        return True

    def execute_movements(self):
        for direction in self.movements:
            self.push(self.robot_coord, direction)

    def GPS_sum(self):
        output = 0
        for i, row in enumerate(self.grid):
            for j, char in enumerate(row):
                if char == "O":
                    output += (100 * i) + j

        return output

    def solve(self):
        self.parse_input()
        self.execute_movements()
        return self.GPS_sum()


class PartTwo(PartOne):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def expand_grid(self):
        """
        Expand the grid as required for the second warehouse
        """
        expanded_grid = []
        for row in self.grid:
            expanded_row = []
            for char in row:
                if char == "@":
                    expanded_row += ["@", "."]
                elif char == "O":
                    expanded_row += ["[", "]"]
                else:
                    expanded_row += [char, char]
            expanded_grid.append(expanded_row)

        self.grid = expanded_grid

    def get_other_box_half(self, coord: list[int], char: str) -> tuple:
        """
        Return the coordinate and character of the other half of a box
        """
        if char == "[":
            return get_next_coord(coord, ">"), "]"
        elif char == "]":
            return get_next_coord(coord, "<"), "["

    def can_push(self, coord: list[int], direction: str) -> bool:
        """
        Return True if pushing the object at coord in the given direction is
            possible, or False otherwise.
        Don't execute the push itself as this may depend on the other half of a
            box being able to move.
        """
        row, col = coord
        char = self.grid[row][col]

        if char == "#":  # Wall
            return False

        if char == ".":  # Free space
            return True

        next_coord = get_next_coord(coord, direction)

        if char == "@" or direction in ["<", ">"]:
            # Only one adjacent char to check
            return self.can_push(next_coord, direction)

        # Pushing a box up or down - need to check its other half as well.
        other_half, _ = self.get_other_box_half(coord, char)
        other_half_next = get_next_coord(other_half, direction)
        return self.can_push(next_coord, direction) and self.can_push(
            other_half_next, direction
        )

    def push(self, coord: list[int], direction: str) -> None:
        """
        Push the object at position (x, y) in the grid in the given direction if possible.
        Do this by first pushing any other objects out of the way.
        Movement is guaranteed as we'll have checked can_push first.
        For boxes, we can push the halves in either order <intuitively obvious but could do with proof>.
        """
        if not self.can_push(coord, direction):
            return

        row, col = coord
        char = self.grid[row][col]

        if char == ".":  # Nothing to push
            return

        # Push the char at this coord regardless of what it is
        next_coord = get_next_coord(coord, direction)
        self.push(next_coord, direction)
        self.grid[next_coord[0]][next_coord[1]] = char
        self.grid[row][col] = "."

        # If this is a box and we're pushing up/down, push the other half too.
        # Prefer explicit code rather than a recursive call and a check for the
        # other half already having moved, as this seems fiddly to debug if it
        # fails.
        if char in ["[", "]"] and direction in ["^", "v"]:
            other_half, other_char = self.get_other_box_half(coord, char)
            other_next = get_next_coord(other_half, direction)
            self.push(other_next, direction)
            self.grid[other_next[0]][other_next[1]] = other_char
            self.grid[other_half[0]][other_half[1]] = "."

        # Update robot position if it moved
        if char == "@":
            self.robot_coord = next_coord

        return

    def GPS_sum(self):
        output = 0
        for i, row in enumerate(self.grid):
            for j, char in enumerate(row):
                if char == "[":
                    output += (100 * i) + j

        return output

    def solve(self):
        self.parse_input()
        self.expand_grid()
        self.find_robot()
        self.execute_movements()
        return self.GPS_sum()


if __name__ == "__main__":
    part_one = PartOne(filename)
    print(part_one.solve())

    part_two = PartTwo(filename)
    print(part_two.solve())
