import fileinput

instructions = []

for line in fileinput.input():
    if len(line.strip()) == 0:
        break
    instructions.append(line.strip())

a = int(instructions[1].split(" ")[1])
b = int(instructions[2].split(" ")[1])

i = a * b
# Clever code dissection reveals the puzzle input basically:
# * Multiplies two constants (a and b)
# * Adds a number (N)
# * And converts it to binary

# We just find a number N that, when added to the constant product, outputs a repeating pattern of 010101010101010s.
while True:
    if "0101010101010101010101010101010101010101".startswith(bin(i)[:2:-1]):
        print(" - The magic value is {} -".format(i - a * b))
        break
    i += 1