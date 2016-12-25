import fileinput
import itertools
import functools

map = []
numbers = {}

for i, line in enumerate(fileinput.input()):
    map.append(line.strip())

    for ii, c in enumerate(line.strip()):
        if c.isdigit():
            numbers[c] = (ii, i)


@functools.lru_cache(1024)
def search(frm, to):
    q = [(0, frm)]
    visited = set()
    while True:
        i, pos = q.pop(0)

        if pos == to:
            return i

        for xx, yy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            nx, ny = (pos[0] + xx, pos[1] + yy)

            if 0 <= nx < len(map[0]) and 0 <= ny < len(map):
                v = map[ny][nx]
                if v != "#" and (nx, ny) not in visited:
                    q.append((i + 1, (nx, ny)))
                    visited.add((nx, ny))


numbers_without_zero = sorted(list(filter(lambda x: x != "0", numbers.keys())))



def find(total_numbers, addendum=()):
    too_slow = []
    smallest = 9999999

    for i, perm in enumerate(itertools.permutations(total_numbers)):
        perm += addendum

        for slow in too_slow:
            if slow == perm[:len(slow)]:
                continue

        total = 0

        n = "0"
        for ii, nn in enumerate(perm):
            best_case_for_remaining = total

            last_remaining = nn
            for remaining in perm[ii + 1:]:
                frm = numbers[last_remaining]
                to = numbers[remaining]

                manhattan = abs(frm[0] - to[0]) + abs(frm[1] - to[1])
                best_case_for_remaining += manhattan

                last_remaining = remaining

            if best_case_for_remaining > smallest or total > smallest:
                too_slow.append(perm[:ii])
                break

            total += search(numbers[n], numbers[nn])
            n = nn
        else:
            if total < smallest:
                smallest = total
    return smallest


print(" - The number of steps to visit every number is {} -".format(find(numbers_without_zero)))
print(" - The number of steps to visit every number (and return) is {} -".format(find(numbers_without_zero, addendum=("0",))))
