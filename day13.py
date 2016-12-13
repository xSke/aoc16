def is_wall(x, y, salt):
  if x < 0 or y < 0:
    return True
    
  num = x*x + 3*x + 2*x*y + y + y*y + salt
  return bin(num).count("1") % 2 != 0
  
def search(start, end, salt, limit=None):
  search_queue = [(0, (start))]
  seen = set()
  seen.add(start)
  
  while True:
    step, pos = search_queue.pop(0)
    
    if (limit and step >= limit) or pos == end:
      break
    
    def add(dx, dy):
      if (pos[0] + dx, pos[1] + dy) in seen:
        return
      
      if not is_wall(pos[0] + dx, pos[1] + dy, salt):
        search_queue.append((step + 1, (pos[0] + dx, pos[1] + dy)))
        seen.add((pos[0] + dx, pos[1] + dy))
        
    add(1, 0)
    add(-1, 0)
    add(0, 1)
    add(0, -1)
    
  return step, seen
  
print("What is the office designer's favorite number?")
salt = int(input(">"))

steps_required, _ = search((1, 1), (31, 39), 1352)
_, locations = search((1, 1), None, 1352, limit=50)

print(" - {} steps are required to reach (31, 39) -".format(steps_required))
print(" - You can reach {} distinct locations in 50 steps -".format(len(locations)))
