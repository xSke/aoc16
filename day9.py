# I'm so sorry...

import fileinput
import re

def decompress(line, part2):
    line = line.strip()

    hit = False
    count = 0
    while True:
        rr = re.match(r, line)
        if rr:
            amnt, times = rr.group(1).split("x")

            line = line[rr.span()[1]:]
            next = line[:int(amnt)]

            if part2:
                count += decompress(next, part2) * int(times)
            else:
                count += len(next) * int(times)

            line = line[int(amnt):]
            hit = True
        else:
            if len(line) == 0:
                break

            line = line[1:]
            count += 1
    return count


r = re.compile(r"\((\d+x\d+)\)")
for line in fileinput.input():
    final = ""

    out = decompress(line, True)
    print(out)
