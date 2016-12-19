def part_1(amount):
    elves = [1] * amount

    while True:
        for i in range(amount):
            if elves[i] > 0:
                left = (i + 1) % amount
                while elves[left] == 0:
                    left = (left + 1) % amount

                elves[i] += elves[left]
                elves[left] = 0

        hit_elf = 0
        for i, elf in enumerate(elves):
            if elf > 0:
                if hit_elf:
                    break

                hit_elf = i
        else:
            return hit_elf + 1


# What the fuck
def part_2():
    last_power_of_three = 0
    counter = 1
    next_power_of_three = 1

    while True:
        yield counter

        if counter < last_power_of_three:
            counter += 1
        else:
            counter += 2

        if counter > next_power_of_three:
            counter = 1
            last_power_of_three = next_power_of_three
            next_power_of_three *= 3


print("How many elves are in the circle?")
elves = int(input(">"))

print(" - The last elf standing when stealing from the left is elf #{} -".format(part_1(elves)))

gen = part_2()
for _ in range(elves):
    value = next(gen)

print(" - The last elf standing when stealing across is elf #{} -".format(value))