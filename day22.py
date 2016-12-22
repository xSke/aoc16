import fileinput
import itertools
import re
import queue

nodes = {}
r = re.compile("/dev/grid/node-x(\d+)-y(\d+)\s+(\d+)T\s+(\d+)T\s+(\d+)T\s+(\d+)%")
for line in fileinput.input():
    m = r.match(line)
    if m:
        x, y, size, used, avail, pct = m.groups()

        nodes[(int(x), int(y))] = (int(size), int(used), int(avail))


def filter_pairs(pair):
    a, b = pair

    a_used = nodes[a][1]
    b_avail = nodes[b][2]
    return a != b and 0 < a_used <= b_avail


combs = itertools.product(nodes.keys(), repeat=2)
valid_pairs = list(filter(filter_pairs, combs))

print(" - The amount of valid pairs is {} -".format(len(valid_pairs)))

mx = (0, 0)
for node in nodes.keys():
    if nodes[node][1] == 0:
        empty_node = node
        empty_size = nodes[node][0]

    mx = (max(node[0], mx[0]), max(node[1], mx[1]))
target_node = (mx[0], 0)


seen = set()
q = [(0, (empty_node, target_node))]
while True:
    i, (e, t) = q.pop(0)

    if t == (0, 0):
        print(" - The minimum amount of moves is {} -".format(i))
        break

    for m in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        ofs = (e[0] + m[0], e[1] + m[1])
        if ofs in nodes and nodes[ofs][1] <= empty_size:
            nt = t
            if ofs == nt:
                nt = e

            if (ofs, nt) not in seen:
                q.append((i + 1, (ofs, nt)))
                seen.add((ofs, nt))