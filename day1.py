direction = "N"
x = 0
y = 0

log = []

for instruction in input("> ").split(", "):
    rotation = instruction[0]
    amount = int(instruction[1:])

    if rotation == "L":
        direction = {"N":"W", "W":"S", "S":"E", "E":"N"}[direction]
    else:
        direction = {"N":"E", "E":"S", "S":"W", "W":"N"}[direction]

    # Do this individually to count ALL points in the log
    for _ in range(amount):
        if direction == "N": y+=1
        if direction == "S": y-=1
        if direction == "E": x-=1
        if direction == "W": x+=1
        log.append((x, y))

print(" - The final location is at ({}, {}) [{} blocks away] -".format(x, y, abs(x) + abs(y)))

# O(n^2) but who cares
for entry in log:
    if log.count(entry) > 1:
        print(" - The first location visited twice is at ({}, {}) [{} blocks away] -".format(*entry, abs(entry[0]) + abs(entry[1])))
        break
