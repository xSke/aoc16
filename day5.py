import itertools, hashlib, sys

spinner = "\|/-"
def progress_print(part1, part2):
    global spinner
    spinner = spinner[1:] + spinner[0]

    print("\r{} - {} {}".format(part1[:8].ljust(8, '_'), "".join(part2), spinner[0]), end="")

key = input("> ")

part1 = ""
part2 = ["_"] * 8

for salt in itertools.count():
    salted_key = key + str(salt)
    hash = hashlib.md5(salted_key.encode("utf8")).hexdigest()

    if hash.startswith("00000"):
        part1 += hash[5]

        pos = int(hash[5], 16)
        if pos < 8 and part2[pos] == "_":
            part2[pos] = hash[6]

            if "_" not in part2:
                break

    if salt % 50000 == 0:
        progress_print(part1, part2)

progress_print(part1, part2)