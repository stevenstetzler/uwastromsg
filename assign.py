from glob import glob # Search for file paths
import os
from random import shuffle

wordspath = 'madlibs/'
gradusernames = os.path.abspath(wordspath + 'gradlist.txt')
gradnames = os.path.abspath(wordspath + 'gradnames.txt') 
bars = os.path.abspath(wordspath + 'bars.txt')
neighborhoods = os.path.abspath(wordspath + 'neighborhoods.txt')
fridays = os.path.abspath(wordspath + 'fridays.txt')

# each friday gets one of everything else 

nfridays = 0
entries = []
with open(fridays, 'r') as fridays:
    for line in fridays:
        nfridays += 1
        entries.append(line.strip() + " ")
        
gu = []
with open(gradusernames) as grads:
    for i, line in enumerate(grads):
        gu.append(line.strip())
            
gn = []           
with open(gradnames) as grads:
    for i, line in enumerate(grads):
        gn.append("\"" + line.strip() + "\"")
            
if len(gu) != len(gn):
    raise Exception("number of grad names does not match number of usernames")

b = []
n = []
with open(bars) as bars, open(neighborhoods) as neighborhoods:
    for line in bars:
        b.append("\"" + line.strip() + "\"")
    for line in neighborhoods:
        n.append("\"" + line.strip() + "\"")

g = [u + " " + n for u, n in zip(gu, gn)]
shuffle(g)
shuffle(b)
shuffle(n)
entries = [g[i % len(g)] + " " + b[i % len(b)] + " " + n[i % len(n)] for i in range(nfridays)]      
        
for line in entries:
    print(line)
        