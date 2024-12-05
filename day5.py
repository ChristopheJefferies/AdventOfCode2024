filename = "input5.txt"
with open(filename) as file:
    input = [line.rstrip() for line in file]

from collections import defaultdict

# Parts 1 and 2

# Process input
separator = input.index("")  # Blank line between rules and updates
rules = defaultdict(set)  # Values are sets of ints which must only appear after the key
for line in input[:separator]:
    int1, int2 = line.split("|")
    int1, int2 = int(int1), int(int2)
    rules[int1].add(int2)


# For part 2
def sort_by_rules(update: list[int]) -> int:
    """
    Return the update after sorting it according to the rules.
    """
    # Approach: find all ints which don't appear in any others' rules.
    # Put them first, then repeat on the rest.

    if len(set(update)) <= 1:
        return update

    leading_ints = set(update)
    for num in set(update):
        leading_ints -= rules[num]

    assert len(leading_ints) > 0, "Loop found in update rules"

    # Include leading ints as many times as they appear in the update
    output = [num for num in leading_ints for _ in range(update.count(num))]
    # Everything else goes after them
    remaining_ints = [i for i in update if not (i in leading_ints)]
    output += sort_by_rules(remaining_ints)

    return output


output = 0
output2 = 0

for line in input[separator + 1 :]:
    update = [int(i) for i in line.split(",")]
    seen_nums = set()
    is_ordered = True

    for num in update:
        if rules[num].intersection(seen_nums):  # Seen an int which should appear later
            is_ordered = False
            break
        seen_nums.add(num)

    # Part 1
    if is_ordered:
        output += update[(len(update) - 1) // 2]  # Assumes each update has odd length

    # Part 2
    else:
        output2 += sort_by_rules(update)[(len(update) - 1) // 2]

print(output)
print(output2)
