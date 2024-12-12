filename = "input12.txt"
with open(filename) as file:
    input = [list(line.rstrip()) for line in file]

MAX_ROW = len(input) - 1
MAX_COL = len(input[0]) - 1

opposite_directions = {"up": "down", "down": "up", "right": "left", "left": "right"}


def is_in_grid(coord: tuple[int]) -> bool:
    return (0 <= coord[0] <= MAX_ROW) and (0 <= coord[1] <= MAX_COL)


def adjacent_coords(coord: tuple[int]) -> dict:
    row, col = coord
    return {
        "up": (row - 1, col),
        "down": (row + 1, col),
        "left": (row, col - 1),
        "right": (row, col + 1),
    }


def update_edges(
    edges: dict,
    coord: tuple,
    adjacent_coord: tuple,
    direction: str,
    same_region: bool,
) -> None:
    """
    Add/remove the relevant edge from an edges dict based on regions
    and adjacency directions. (Modifies edges in-place)
    Edges are labelled with the coord below or to the right of them, regardless
    of whether that coord is in the grid/region.
    """

    if not same_region:  # Add the new external edge
        if direction in ["up", "left"]:  # Label the edge with this coord
            edges[direction].add(coord)
        else:  # Label the edge with the adjacent coord (below/right)
            edges[direction].add(adjacent_coord)

    else:  # Remove the now-internal edge
        # Flip direction as the edge was labelled from the other side
        direction = opposite_directions[direction]
        if direction in ["down", "right"]:
            edges[direction].remove(coord)
        else:
            edges[direction].remove(adjacent_coord)


def num_sides(region: dict) -> int:
    """
    region is a dictionary with keys 'up', 'down', 'right', 'left'. Each value is
    a set of coordinates.
    Returns the total number of sides formed by these edge segments (where edges
    with different directions do not join).
    This is a janky approach but good enough for a rushed AOC before I go out.
    """
    output = 0

    for coords in [region["left"], region["right"]]:  # Vertical sides
        while coords:
            output += 1
            coord = coords.pop()

            for move in [1, -1]:
                row, col = coord
                row += move
                while (row, col) in coords:
                    coords.remove((row, col))
                    row += move

    for coords in [region["up"], region["down"]]:  # Horizontal sides
        while coords:
            output += 1
            coord = coords.pop()

            for move in [1, -1]:
                row, col = coord
                col += move
                while (row, col) in coords:  # Remove edge segments left
                    coords.remove((row, col))
                    col += move

    return output


price1, price2 = 0, 0
coords_in_new_regions = {(0, 0)}
all_regions = set()

while coords_in_new_regions:  # Whole grid not yet explored
    region = set()
    edges = {"up": set(), "down": set(), "left": set(), "right": set()}

    first_coord = coords_in_new_regions.pop()
    region_char = input[first_coord[0]][first_coord[1]]
    coords_to_look_around = {first_coord}

    while coords_to_look_around:  # Whole region not yet found
        coord = coords_to_look_around.pop()

        for direction, adj_coord in adjacent_coords(coord).items():
            # Record edges against the border of the grid
            if not is_in_grid(adj_coord):
                update_edges(edges, coord, adj_coord, direction, False)

            # Update edge segments and record if this adj_coord should be revisited later (in this region or another)
            elif input[adj_coord[0]][adj_coord[1]] == region_char:  # Same region
                if adj_coord in region:  # Already added
                    update_edges(edges, coord, adj_coord, direction, True)
                else:
                    update_edges(edges, coord, adj_coord, direction, False)
                    coords_to_look_around.add(adj_coord)

            else:  # Different region
                update_edges(edges, coord, adj_coord, direction, False)
                coords_in_new_regions.add(adj_coord)

        # Add this coord to the region and update perimeta length/types
        region.add(coord)

    # Region is finished
    price1 += len(region) * sum(len(edge_set) for edge_set in edges.values())
    price2 += len(region) * num_sides(edges)
    all_regions |= region
    coords_in_new_regions -= all_regions

print(price1)
print(price2)
