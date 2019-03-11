from __future__ import print_function
import subprocess
import glob
import sys
import os
import random
import time

try:
    os.mkdir("424mutants")
except:
    pass

CONTRACTS_DIR = "424contracts/"
CONTRACTS = sorted(glob.glob(CONTRACTS_DIR + "*.sol"))

random.seed(1)
random.shuffle(CONTRACTS)

CONTRACTS = CONTRACTS[:100]

already_done = []
if os.path.exists("424.analyzed.slither.txt"):
    with open("424.analyzed.slither.txt", 'r') as finished:
        for line in finished:
            already_done.append(line[:-1])

slots = {}
maxSlots = 6
outFiles = {}

for i in range(0, maxSlots):
    slots[i] = None
    outFiles[i] = open("out." + str(i) + ".txt", 'w')

for C in CONTRACTS:
    if C in already_done:
        print("ALREADY ANALYZED", C)        
        continue
    if os.path.exists(C + ".done"):
        print("ALREADY MUTATED", C)
        continue
    subprocess.call(["rm -rf " + C.replace("424contracts","424mutants").replace(".sol", "*.sol")],
                        shell=True)
    loc = 0
    with open(C) as contractf:
        for line in contractf:
            loc += 1
    running = False
    while not running:
        someEmpty = False
        for i in range(0, maxSlots):
            if (slots[i] is None) and not running:
                P = subprocess.Popen(["mutate", C, "--mutantDir", "424mutants"],
                                         stdout=outFiles[i], stderr=outFiles[i])
                print("STARTING GENERATION OF MUTANTS FOR", C, "WITH", loc, "LINES OF CODE IN SLOT", i)
                slots[i] = (P, C, loc)
                running = True
            elif slots[i] is not None:
                (P, contract, cloc) = slots[i]
                if P.poll() is not None:
                    print("*"*40)
                    print("DONE GENERATING MUTANTS FOR", contract, "IN SLOT", i)
                    print("*"*40)                                        
                    with open(contract + ".done", 'w') as outf:
                        outf.write("DONE\n")
                    slots[i] = None
                else:
                    last = "NOT STARTED YET"
                    with open("out." + str(i) + ".txt", 'r') as outf:
                        for l in outf:
                            last = l[:-1]
                    print("#" + str(i) + ":", contract, "(" + str(cloc) + "):", end="")
                    print(last)
            if slots[i] is None:
                someEmpty = True
        if not someEmpty: # sleep if everything is full
            print("="*80)
            time.sleep(60)
