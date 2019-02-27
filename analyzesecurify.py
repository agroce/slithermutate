from __future__ import print_function
import subprocess
import glob
import sys
import scipy
import scipy.stats
import os
from runsecurify import *

try:
    os.mkdir("mutants")
except:
    pass

scores = []
cleanScores = []
cleanContracts = []

for C in glob.glob("contracts/*.sol"):
    print("="*80)
    print("analyzing", C)
    with open("out.txt", 'w') as outf:
        numIssues = runSecurify(C)
    print("ISSUES:", numIssues)

    sys.stdout.flush()
    if not os.path.exists(C.replace("contracts/", "mutants/").replace(".sol", ".mutant.0.sol")):
        print("GENERATING MUTANTS...")
        with open("out.txt", 'w') as outf:
            r = subprocess.call(["mutate", C, "--mutantDir", "mutants"],
                                    stdout=outf, stderr=outf)
        with open("out.txt", 'r') as outf:
            for line in outf:
                if "MUTANTS" in line:
                    print(line, end=" ")
                    if " VALID MUTANTS" in line:
                        numMutants = int(line.split()[0])
    else:
        numMutants = len(glob.glob(C.replace("contracts/",
                                             "mutants/").replace(".sol",
                                                                 ".mutant.*.sol")))
        print(numMutants, "MUTANTS FOR CONTRACT FOUND")    
    sys.stdout.flush()
    if numMutants == 0:
        print("NO VALID MUTANTS, SKIPPING...")
        continue
    with open("out.txt", 'w') as outf:
        subprocess.call(["analyze_mutants", C, "python maxissuessecurify.py " +
                             str(numIssues) + " " + C,
                             "--mutantDir", "mutants"],
                            stdout=outf, stderr=outf)
    with open("out.txt", 'r') as outf:
        for line in outf:
            if "MUTATION SCORE" in line:
                print(line, end=" ")
                score = float(line.split()[-1])
    subprocess.call(["wc","-l","killed.txt"])
    subprocess.call(["wc","-l","notkilled.txt"])
    sys.stdout.flush()    
    subprocess.call(["cp","killed.txt",C+".securify.killed.txt"])
    subprocess.call(["cp","notkilled.txt",C+".securify.notkilled.txt"])
    scores.append(score)
    if numIssues == 0:
        cleanScores.append(score)
        cleanContracts.append(C)

print("*"*80)
print()
print("SCORES:", scores, len(scores), "ANALYZED")
print("  MEAN:", scipy.mean(scores))
print("  MEDIAN:", scipy.median(scores))
print("  STD:", scipy.std(scores))

print("*"*80)
print()
print("CLEAN CONTRACT SCORES:", cleanScores, len(cleanScores), "ANALYZED")
print("CLEAN CONTRACTS:", cleanContracts)
print("  MEAN:", scipy.mean(cleanScores))
print("  MEDIAN:", scipy.median(cleanScores))
print("  STD:", scipy.std(cleanScores))
