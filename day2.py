filename = "input2.txt"
with open(filename) as file:
    input = [line.rstrip() for line in file]

# Part 1
output = 0


def is_safe(report: list[int]) -> bool:
    """
    Return True if the list is strictly increasing/decreasing and by at most 3
    at a time, else False
    """

    # Only consider ascending lists
    if report[1] < report[0]:
        report = report[::-1]

    for i in range(1, len(report)):
        if report[i] - report[i - 1] not in [1, 2, 3]:
            return False

    return True


for line in input:
    report = [int(i) for i in line.split()]
    output += is_safe(report)

print(output)


# Part 2


def is_safe_with_removal(report: list[int]) -> bool:
    """
    Return True if removing (up to) one item leaves the report safe, else False
    """
    if is_safe(report):
        return True

    for i in range(len(report)):
        if is_safe(report[:i] + report[i + 1 :]):
            return True

    return False


output2 = 0

for line in input:
    report = [int(i) for i in line.split()]
    output2 += is_safe_with_removal(report)

print(output2)
