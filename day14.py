import hashlib
import functools

def contains_seq(str, amount):
  for i, c in enumerate(str):
    if str[i:i+amount] == c*amount:
      return c
  
@functools.lru_cache(maxsize=2048)
def hash(salt, nonce, stretch=False):
  hash = hashlib.md5((salt + str(nonce)).encode("utf-8")).hexdigest()
  
  if stretch:
    for _ in range(2016):
      hash = hashlib.md5(hash.encode("utf-8")).hexdigest()
      
  return hash
      
def pads(salt, stretch=False):
  nonce = 0
  
  while True:
    h = hash(salt, nonce, stretch)
    
    c = contains_seq(h, 3)
    if c:
      for n2 in range(1, 1000):
        h2 = hash(salt, nonce + n2, stretch)
        if c*5 in h2:
          yield nonce, h
          break
        
    nonce += 1
    
print("What is the pre-arranged salt?")
salt = input(">")

i = 0
for idx, pad in pads(salt, False):
  i += 1
  if i == 64:
    print(" - The 64th key index (without key-stretching) is {} -".format(idx))
    break
  
i = 0
for idx, pad in pads(salt, True):
  i += 1
  if i == 64:
    print(" - The 64th key index (with key-stretching) is {} -".format(idx))
    break
