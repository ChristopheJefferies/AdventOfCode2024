from collections import Counter

filename = "input1.txt"
with open(filename) as file:
    input = [line.rstrip() for line in file]

# Part 1

# Parse input in to lists of ints
left, right = [], []
for line in input:
    left_num, right_num = line.split()
    left.append(int(left_num))
    right.append(int(right_num))

# Sorting and zipping compares the relevant ints
output = 0
for (a, b) in zip(sorted(left), sorted(right)):
    output += abs(a - b)

print(output)

# Part 2

# Counters let us handle all instances of each int at once
left_count = Counter(left)
right_count = Counter(right)

output2 = 0
for left_num in left_count:
    if left_num in right_count:
        output2 += left_num * left_count[left_num] * right_count[left_num]

print(output2)