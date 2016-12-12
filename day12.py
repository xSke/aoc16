import fileinput

registers = {"a":0, "b":0, "c":0, "d":0}

def value(val):
  try:
    return int(val)
  except ValueError:
    return registers[val]

def run(instruction, current_pc):
  params = instruction.split(" ")
  
  if params[0] == "cpy":
    registers[params[2]] = value(params[1])
  elif params[0] == "inc":
    registers[params[1]] += 1
  elif params[0] == "dec":
    registers[params[1]] -= 1
  elif params[0] == "jnz":
    if value(params[1]) != 0:
      return current_pc + int(params[2])
  return current_pc + 1
  
instructions = []
pc = 0

for line in fileinput.input():
  if len(line.strip()) == 0:
    break
  instructions.append(line.strip())

while pc < len(instructions):
  pc = run(instructions[pc], pc)
print(" - The value in register a is {} -".format(registers["a"]))

registers = {"a":0, "b":0, "c":1, "d":0}
pc = 0
while pc < len(instructions):
  pc = run(instructions[pc], pc)
print(" - The value in register a (with c=1) is {} -".format(registers["a"]))
