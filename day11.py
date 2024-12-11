filename = "input11.txt"
with open(filename) as file:
    input = file.read()

from collections import defaultdict

# Part 1


def blink_once(stones: list[str]) -> list[str]:
    output = []

    for stone in stones:
        if stone == "0":
            output.append("1")
            continue

        L = len(stone)
        if L % 2 == 0:
            output.append(str(int(stone[: L // 2])))
            output.append(str(int(stone[L // 2 :])))

        else:
            output.append(str(2024 * int(stone)))

    return output


stones = input.split()

for i in range(25):
    stones = blink_once(stones)

print(len(stones))


# Part 2
# For this to run in reasonable time, we should treat each stone separately at
# each step rather than calculating the whole list of stones, and use a cache.

# Keys are stone numbers, values are dicts like {iterations: num_stones}
cache = defaultdict(dict)


def iterate_stone(stone: int, iterations: int) -> int:
    """
    Return the final number of stones when starting with one stone and blinking
    the given number of times.
    """

    if iterations == 0:  # No use storing lots of 0's in the cache
        return 1

    if stone in cache:
        if iterations in cache[stone]:
            return cache[stone][iterations]

    output = 0
    next_stones = blink_once([stone])
    for next_stone in next_stones:
        output += iterate_stone(next_stone, iterations - 1)

    cache[stone][iterations] = output
    return output


stones = input.split()
num_iterations = 75
output = 0

for stone in stones:
    output += iterate_stone(stone, num_iterations)

print(output)
