filename = "input3.txt"
with open(filename) as file:
    input = [line.rstrip() for line in file]

# Part 1
import re

pattern = r"mul\(\d{1,3},\d{1,3}\)"  # Strings like "mul(12,345)"
output = 0

for line in input:
    for match in re.finditer(pattern, line):
        int1, int2 = match.group()[4:-1].split(
            ","
        )  # Trim the 'mul(' and final ')', then ignore the comma
        output += int(int1) * int(int2)
print(output)

# Part 2

pattern2 = pattern + r"|(do|don't)\(\)"  # Also catch "do()" and "don't()"
output2 = 0
do = True

for line in input:
    for match in re.finditer(pattern2, line):
        # do()
        if match.group()[2] == "(":
            do = True

        # don't()
        elif match.group()[0] == "d":
            do = False

        else:  # mul
            if do:
                int1, int2 = match.group()[4:-1].split(
                    ","
                )  # Trim the 'mul(' and final ')', then ignore the comma
                output2 += int(int1) * int(int2)

print(output2)
