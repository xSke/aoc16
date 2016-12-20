import fileinput
from functools import reduce


def contains(range, val):
    if isinstance(val, tuple):
        return range[0] <= val[0] and val[1] <= range[1]
    else:
        return range[0] <= val <= range[1]


def merge_spans(spans):
    # http://stackoverflow.com/a/9219395

    spans = sorted(spans, key=lambda x: x[0])

    def reducer(acc, span):
        if contains(acc[0], span):
            # Complete overlap
            return acc
        elif contains(acc[0], span[0]) or span[0] == acc[0][1] + 1:
            # Partial overlap (or touch)
            return [(acc[0][0], span[1])] + acc[1:]
        else:
            # No overlap
            return [span] + acc

    return reduce(reducer, spans, [spans[0]])[::-1]


blocklist = list(fileinput.input())
spans = []
for b in blocklist:
    first = int(b.split("-")[0])
    second = int(b.split("-")[1])

    spans.append((first, second))

spans = merge_spans(spans)
print(" - The first IP address that isn't blocked is {} -".format(spans[0][1] + 1))

total_unblocked = 2 ** 32
for start, end in spans:
    total_unblocked -= (end - start + 1)
print(" - There are a total of {} unblocked IP addresses -".format(total_unblocked))
