import re
import fileinput

def contains_abba(str):
  for i in range(len(str)-3):
    slice = str[i:i+4]
    if slice[0] != slice[1] and slice[0:2] == slice[4:1:-1]:
      return True
      
  return False
  
def find_abas(lst):
  for str in lst:
    for i in range(len(str)-2):
      slice = str[i:i+3]
  
      if slice[0] == slice[2] and slice[0] != slice[1]:
        yield slice
      
def flip(aba):
  return aba[1] + aba[0] + aba[1]
      
def matches_babs(supernets, hypernets):
  abas = find_abas(supernets)
  babs = " ".join(hypernets)
  
  for aba in abas:
    if flip(aba) in babs:
      return True
  return False
  
tls_count = 0
ssl_count = 0
for line in fileinput.input():
  line = line.strip()
  if len(line) == 0:
    break
  
  groups = re.split(r"[\[\]]", line)
  supernets = groups[0::2]
  hypernets = groups[1::2]
  
  supports_tls = contains_abba(" ".join(supernets)) and not contains_abba(" ".join(hypernets))
  if supports_tls:
    tls_count += 1
    
  supports_ssl = matches_babs(supernets, hypernets)
  if supports_ssl:
    ssl_count += 1
  
print(" - {} IPs support TLS -".format(tls_count))
print(" - {} IPs support SSL -".format(ssl_count))
