import fileinput

def value(val):
    try:
        return int(val)
    except ValueError:
        return registers[val]


def run(instruction, current_pc, instructions, registers):
    params = instruction.split(" ")

    if params[0] == "cpy":
        if not params[2].isdigit():
            registers[params[2]] = value(params[1])
    elif params[0] == "inc":
        if not params[1].isdigit():
            registers[params[1]] += 1
    elif params[0] == "dec":
        if not params[1].isdigit():
            registers[params[1]] -= 1
    elif params[0] == "jnz":
        if value(params[1]) != 0:
            return current_pc + value(params[2])
    elif params[0] == "tgl":
        edit_index = current_pc + value(params[1])
        if edit_index < len(instructions):
            ins = instructions[edit_index]
            params = ins.split(" ")
            if params[0] == "inc":
                params[0] = "dec"
            elif params[0] == "dec" or params[0] == "tgl":
                params[0] = "inc"
            elif params[0] == "cpy":
                params[0] = "jnz"
            elif params[0] == "jnz":
                params[0] = "cpy"
            instructions[edit_index] = " ".join(params)
    elif params[0] == "mul":
        res = value(params[1]) * value(params[2])
        registers[params[3]] = res

    return current_pc + 1

def run_code(instructions, registers):
    instructions = list(instructions)
    pc = 0
    while pc < len(instructions):
        pc = run(instructions[pc], pc, instructions, registers)

instructions = []

for line in fileinput.input():
    if len(line.strip()) == 0:
        break
    instructions.append(line.strip())

# Ha ha ha
# You do not fool me, easter bunny
# (these instructions optimize to a multiply)
instructions = "\n".join(instructions).replace("cpy b c\ninc a\ndec c\njnz c -2\ndec d\njnz d -5", "nop\nnop\nnop\nnop\nnop\nmul b d a").split("\n")

registers = {"a": 7, "b": 0, "c": 0, "d": 0}
run_code(instructions, registers)
print(" - The value in register a (7 eggs) is {} -".format(registers["a"]))

registers = {"a": 12, "b": 0, "c": 0, "d": 0}
run_code(instructions, registers)
print(" - The value in register a (12 eggs) is {} -".format(registers["a"]))

