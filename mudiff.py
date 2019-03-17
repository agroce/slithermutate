import glob
import subprocess
import Levenshtein

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
    code = []
    with open(original, 'r') as ofile:
        for l in ofile:
            code.append(l)
    for m in nk:
        mcode = []
        lno = 0
        with open("424mutants/" + m, 'r') as mfile:
            for l in mfile:
               mcode.append(l)
               if mcode[lno] != code[lno]:
                   diff = (code[lno], mcode[lno], lno)
                   break
               lno += 1
        (origCode, mutantCode, lineno) = diff
        if m not in nkslither:
            smartwins.append((m, origCode, mutantCode, lineno))

dcache = {}

def changed(orig, mutant):
    eops = Levenshtein.editops(orig,mutant)
    blocks = Levenshtein.matching_blocks(eops, orig, mutant)
    if len(blocks) > 4:
        return mutant
    keep = ''.join([orig[x[0]:x[0]+x[2]] for x in blocks])
    notkeep = ""
    pos = 0
    wasDot = False
    for c in range(0,len(orig)):
        if orig[c] == keep[pos]:
            pos += 1
            if not wasDot:
                notkeep += "..."
                wasDot = True
        else:
            notkeep += orig[c]
            wasDot = False
    notkeep += "==>"
    pos = 0
    wasDot = False
    for c in range(0,len(mutant)):
        if mutant[c] == keep[pos]:
            pos += 1
            if not wasDot:
                notkeep += "..."
                wasDot = True
        else:
            notkeep += mutant[c]
            wasDot = False            
    return notkeep

def d(m1,m2):
    global dcache
    if m1 == m2:
        return 0
    if (m1, m2) in dcache:
        return dcache[(m1, m2)]
    (mfile1, orig1, mutant1, lineno1) = m1
    (mfile2, orig2, mutant2, lineno2) = m2
    mchange1 = changed(orig1, mutant1)
    mchange2 = changed(orig2, mutant2)
    dm1m2 = Levenshtein.distance(mchange1,mchange2)
    mchange1 = orig1 + "==>" + mutant1
    mchange2 = orig2 + "==>" + mutant2   
    dm1m2 += 0.1 * Levenshtein.distance(mchange1,mchange2)    
    dcache[(m1, m2)] = dm1m2
    return dm1m2

def show(m):
    (mfile, orig, mutant, lineno) = m
    print "="*80
    print mfile
    print orig[:-1]
    print " ==> "
    print mutant[:-1]
    print "CHANGE:", changed(orig, mutant)
            
shown = [smartwins[0]]

show(smartwins[0])

while len(shown) < 50:
    best = None
    maxMin = -1
    for m1 in smartwins:
        smallest = -1
        for m2 in shown:
            dm1m2 = d(m1,m2)
            if (smallest == -1) or (dm1m2 < smallest):
                smallest = dm1m2
        if smallest > maxMin:
            best = m1
            maxMin = smallest
    print "*"*80
    print "new distance", maxMin
    show(best)
    shown.append(best)
