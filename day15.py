import sys


def pos_at(positions, time, start, offset):
    return (start + time + offset) % positions


def can_drop(discs, time):
    for i, disc in enumerate(discs):
        if pos_at(disc[0], time, disc[1], i + 1) != 0:
            return False
    return True


def parse_input(lines):
    for line in lines:
        tokens = line.strip().split(" ")
        yield int(tokens[3]), int(tokens[11][:-1])


def valid_positions(discs):
    t = 0
    while True:
        if can_drop(discs, t):
            yield t
        t += 1


discs = list(parse_input(sys.stdin))

first_t = next(valid_positions(discs))
print(" - Pressing the button at t={} will drop a capsule -".format(first_t))

second_t = next(valid_positions(discs + [(11, 0)]))
print(" - Pressing the button again at t={} will drop a capsule -".format(second_t))
