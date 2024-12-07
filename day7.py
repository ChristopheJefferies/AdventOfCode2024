filename = "input7.txt"
with open(filename) as file:
    input = [line.rstrip() for line in file]

output = 0
output2 = 0

for line in input:
    nums = line.split()
    target = int(nums[0][:-1])  # Strip off colon
    nums = [int(i) for i in nums[1:]]

    possible_vals = {nums[0]}
    possible_vals2 = {nums[0]}
    for num in nums[1:]:
        sums1 = {i + num for i in possible_vals if i + num <= target}
        prods1 = {i * num for i in possible_vals if i * num <= target}
        possible_vals = sums1.union(prods1)

        str_num = str(num)
        sums2 = {i + num for i in possible_vals2 if i + num <= target}
        prods2 = {i * num for i in possible_vals2 if i * num <= target}
        concats2 = {int(str(i) + str_num) for i in possible_vals2}
        concats2 = {i for i in concats2 if i <= target}
        possible_vals2 = sums2.union(prods2).union(concats2)

    if target in possible_vals:
        output += target

    if target in possible_vals2:
        output2 += target

print(output)
print(output2)
