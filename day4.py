import collections
import fileinput
import re

r = re.compile(r"([\w\-]+)\-([\d]+)\[([\w]{5})\]")

def calculate_checksum(line):
    line = name.replace("-", "")
    counter = collections.Counter(line)

    line = list(set(line))    
    line = sorted(line)
    line = sorted(line, key=lambda x: -counter[x])
    return "".join(line[:5])

def decrypt(line, rounds):
    output = ""
    for c in line:
        val = ord(c)
        if 97 <= val <= 122:
            output += chr((val - 97 + rounds) % 26 + 97)
        else:
            output += c
    return output.replace("-", " ")


sector_total = 0
for line in fileinput.input():
    name, sector, checksum = r.search(line).groups()
    sector = int(sector)
    sector_total += sector
    
    calculated_checksum = calculate_checksum(checksum)
    decrypted_name = decrypt(name, sector)

    if decrypted_name == "northpole object storage":
        northpole_sector = sector

print(" - The sum of all the valid rooms' sector IDs is {} - ".format(sector_total))
print(" - The room with the North Pole objects is in sector {} - ".format(northpole_sector))
