import hashlib


def open_doors(pos, path, passcode):
    hash = hashlib.md5((passcode + path).encode("utf-8")).hexdigest()[:4]
    open = [x for i, x in enumerate("UDLR") if hash[i] in "bcdef"]
    if pos[1] == 0 and "U" in open:
        open.remove("U")
    if pos[1] == 3 and "D" in open:
        open.remove("D")
    if pos[0] == 0 and "L" in open:
        open.remove("L")
    if pos[0] == 3 and "R" in open:
        open.remove("R")

    return "".join(open)


def adj_pos(pos, dir):
    if dir == "U":
        return pos[0], pos[1] - 1
    if dir == "D":
        return pos[0], pos[1] + 1
    if dir == "L":
        return pos[0] - 1, pos[1]
    if dir == "R":
        return pos[0] + 1, pos[1]


def paths(passcode):
    open_queue = [((0, 0), "")]

    while len(open_queue) > 0:
        pos, path = open_queue.pop(0)
        if pos == (3, 3):
            yield path
        else:
            for door in open_doors(pos, path, passcode):
                open_queue.append((adj_pos(pos, door), path + door))


print("What is the passcode of the vault?")
passcode = input(">")

print(" - The shortest path to the vault is {} -".format(next(paths(passcode))))

for path in paths(passcode):
    pass  # "path" doesn't go out of scope here cause python so it'll be the last value

print(" - The longest path to the vault is {} -".format(len(path)))
