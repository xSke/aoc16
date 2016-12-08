import fileinput

def rect(data, w, h):
  for y in range(h):
    for x in range(w):
      data[y][x] = "#"

def rotcol(data, x, amount):
  col = [data[y][x] for y in range(6)]
  for y in range(6):
    data[y][x] = col[(y - amount) % 6]

def rotrow(data, y, amount):
  amount %= 50
  data[y] = data[y][-amount:] + data[y][0:-amount]

data = [[" "] * 50 for _ in range(6)] 
for line in fileinput.input():
  if len(line.strip()) == 0:
    break
  
  words = line.strip().split(" ")
  
  if words[0] == "rect":
    parts = words[1].split("x")
    rect(data, int(parts[0]), int(parts[1]))
  elif words[0] == "rotate" and words[1] == "column":
    rotcol(data, int(words[2][2:]), int(words[4]))
  elif words[0] == "rotate" and words[1] == "row":
    rotrow(data, int(words[2][2:]), int(words[4]))

final = "\n".join(["".join(x) for x in data])
print(" - {} pixels are on -".format(final.count("#")))
print(final)
