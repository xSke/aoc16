import re


def fill_step(input):
    other = input[::-1].replace("0", "x").replace("1", "0").replace("x", "1")
    return input + "0" + other


def fill_until(input, amount):
    while len(input) < amount:
        input = fill_step(input)
    return input[:amount]

def checksum(input):
    if len(input) % 2 == 1:
        return input

    groups = ["1" if x[0] == x[1] else "0" for x in re.findall('..', input)]
    return checksum("".join(groups))

print("What is the initial state of the disk?")
initial_state = input(">")

final_sum = checksum(fill_until(initial_state, 272))
print(" - The checksum of the first disk is {} -".format(final_sum))

final_sum = checksum(fill_until(initial_state, 35651584))
print(" - The checksum of the second disk is {} -".format(final_sum))

