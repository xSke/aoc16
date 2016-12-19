def next_row(previous_row):
    last = ["."] + previous_row + ["."]
    return ["^" if last[i] != last[i + 2] else "." for i in range(len(previous_row))]


def get_rows(row):
    yield row

    while True:
        row = next_row(row)
        yield row


def safe_count(starting, amount):
    row_gen = get_rows(list(starting))

    count = 0
    for row in (next(row_gen) for _ in range(amount)):
        count += row.count(".")

    return count


print("What is the initial row of traps?")
starting = input(">")

print(" - There are {} safe tiles in the first 40 rows -".format(safe_count(starting, 40)))
print(" - There are {} safe tiles in the first 400000 rows -".format(safe_count(starting, 400000)))
