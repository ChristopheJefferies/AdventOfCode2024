filename = "input9.txt"
with open(filename) as file:
    input = file.read()

input = [int(i) for i in list(input)]

# Part 1
# Go straight to the answer with a two-pointer method

output = 0
front_idx = 0  # Steps through files and gaps from the front
back_idx = -1  # Steps through files only, from the back
front_file_ID = 0
back_file_ID = (len(input) - 1) // 2  # Input assumed to be of odd length
front_remaining = input[0]
back_remaining = input[-1]
is_file = True  # False when front pointer is looking at a gap

for write_position in range(sum(input[::2])):
    if is_file:  # Grab a digit from the front
        output += write_position * front_file_ID
        front_remaining -= 1

        if not front_remaining:  # Reached the end of this file at the front
            front_idx += 1
            front_file_ID += 1
            front_remaining = input[front_idx]
            is_file = False

    else:  # Grab a digit from the back
        output += write_position * back_file_ID
        back_remaining -= 1
        front_remaining -= 1

        if not back_remaining:  # Used up a whole file at the back
            back_idx -= 2  # Jump over a gap as we don't grab digits from those
            back_file_ID -= 1
            back_remaining = input[back_idx]

        if not front_remaining:  # Reached the end of this gap at the front
            front_idx += 1
            front_remaining = input[front_idx]
            is_file = True

    while front_remaining == 0:  # We've hit files/gaps of length 0 - skip them
        front_idx += 1
        front_remaining = input[front_idx]
        is_file = not is_file

print(output)


# Part 2
# Step through and fill gaps with the latest available file which fits

num_files = (len(input) + 1) // 2
file_lengths = {i: input[2 * i] for i in range(num_files)}
available_files = set(range(num_files))
front_idx = 0  # Index in the input of file/gap we're looking at

checksum = 0
position = 0

while True:
    # Handle a file
    file_ID = front_idx // 2  # Halve due to gaps
    if file_ID in available_files:  # It hasn't been grabbed to fill an earlier gap
        for _ in range(file_lengths[file_ID]):
            checksum += position * file_ID
            position += 1
        available_files.remove(file_ID)  # No longer available for filling future gaps
    else:
        position += file_lengths[file_ID]
    front_idx += 1

    if front_idx == len(input):  # Reached the end
        break

    # Handle a gap. Find the latest files which fit (if any)
    gap_remaining = input[front_idx]  # Prepare to track next gap size
    for later_file in sorted(available_files, reverse=True):

        if file_lengths[later_file] <= gap_remaining:
            # It fits in the gap we're considering
            for _ in range(file_lengths[later_file]):
                checksum += position * later_file
                position += 1

            gap_remaining -= file_lengths[later_file]
            available_files.remove(
                later_file
            )  # No longer available for filling future gaps

        if gap_remaining == 0:  # Clearly can't fit any more files in this gap
            break

    # Restart loop on next file
    position += gap_remaining
    front_idx += 1

print(checksum)
