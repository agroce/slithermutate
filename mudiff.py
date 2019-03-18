import glob
import subprocess
from universalmutator.utils import *

smartwins = []

for f in glob.glob("424contracts/*.smartcheck.killed.txt"):
    original = f.replace(".smartcheck.killed.txt", "")
    nk = []
    with open(f, 'r') as nkfile:
        for l in nkfile:
            nk.append(l[:-1])
    nkslither = []
    with open(f.replace("smartcheck","slither"), 'r') as nkfile:
        for l in nkfile:
            nkslither.append(l[:-1])    
    for m in nk:
        if m not in nkslither:
            smartwins.append(readMutant(m, original, mutantDir="424mutants"))
            
ranked = FPF(smartwins, 10)
print ranked

for (r, d) in ranked:
    print "*"*80
    show(r)
    print "distance:", d
