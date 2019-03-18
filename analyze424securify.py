from __future__ import print_function
import subprocess
import glob
import sys
import scipy
import scipy.stats
import os
import random
from runsecurify import *

try:
    os.mkdir("424mutants")
except:
    pass

scores = []
issues = []
cleanScores = []
cleanContracts = []

CONTRACTS_DIR = "424contracts/"
CONTRACTS = sorted(glob.glob(CONTRACTS_DIR + "*.sol"))

random.seed(1)
random.shuffle(CONTRACTS)

CONTRACTS = CONTRACTS[:100] # just first 100 for first run

already_done = []
if os.path.exists("424.analyzed.securify.txt"):
    with open("424.analyzed.securify.txt", 'r') as finished:
        for line in finished:
            already_done.append(line[:-1])

for C in CONTRACTS:
    print("="*80)
    print("analyzing", C)
    loc = 0
    with open(C) as contractf:
        for line in contractf:
            loc += 1
    print("  LOC:", loc)
    if C in already_done:
        print("already analyzed")
        with open(C+".securify.issues", 'r') as issuef:
            numIssues = int(issuef.read())
        print("ISSUES:", numIssues)
        if numIssues == -1:
            print("SECURIFY FAILED")
            continue
        if os.path.exists(C+".securify.killed.txt"):
            killedCount = 0
            notKilledCount = 0
            with open(C+".securify.killed.txt", 'r') as killed:
                for line in killed:
                    killedCount += 1
            with open(C+".securify.notkilled.txt", 'r') as notKilled:
                for line in notKilled:
                    notKilledCount += 1
            print(killedCount + notKilledCount, "VALID MUTANTS")
            print(killedCount, "killed.txt")
            print(notKilledCount, "notkilled.txt")
            score = float(killedCount)/float(killedCount+notKilledCount)
            print("MUTATION SCORE:", score)
        else:
            print("NO VALID MUTANTS")
            continue
    else:
        with open("out.txt", 'w') as outf:
            numIssues = runSecurify(C)
        with open("out.txt", 'r') as outf:
            results = outf.read()
        print("ISSUES:", numIssues)
        with open(C+".securify.issues", 'w') as issuef:
            issuef.write(str(numIssues)+"\n")
        sys.stdout.flush()
        if not os.path.exists(C.replace(CONTRACTS_DIR, "424mutants/").replace(".sol", ".mutant.0.sol")):
            print("GENERATING MUTANTS...")
            with open("out.txt", 'w') as outf:
                r = subprocess.call(["mutate", C, "--mutantDir", "424mutants"],
                                        stdout=outf, stderr=outf)
            with open("out.txt", 'r') as outf:
                for line in outf:
                    if "MUTANTS" in line:
                        print(line, end=" ")
                        if " VALID MUTANTS" in line:
                            numMutants = int(line.split()[0])
        else:
            numMutants = len(glob.glob(C.replace(CONTRACTS_DIR,
                                                 "424mutants/").replace(".sol",
                                                                     ".mutant.*.sol")))
            print(numMutants, "MUTANTS FOR CONTRACT FOUND")
        sys.stdout.flush()
        if numMutants == 0:
            print("NO VALID MUTANTS, SKIPPING...")
            continue
        with open("out.txt", 'w') as outf:
            subprocess.call(["analyze_mutants", C, "python maxissuessecurify.py " +
                                 str(numIssues) + " " + C,
                                 "--mutantDir", "424mutants",
                                 "--timeout", "3600", "--resume"],
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
        with open("424.analyzed.securify.txt", 'a') as finished:
            finished.write(C + "\n")
    scores.append(score)
    issues.append(numIssues)
    if numIssues == 0:
        cleanScores.append(score)
        cleanContracts.append(C)
    print()
    print("RUNNING TOTALS ON", len(scores), "CONTRACTS /", len(cleanScores), "CLEAN CONTRACTS")
    print("ISSUES MEAN:", scipy.mean(issues), "MEDIAN:", scipy.median(issues), "STD:", scipy.std(issues))        
    print("MUTANTS MEAN:", scipy.mean(scores), "MEDIAN:", scipy.median(scores), "STD:", scipy.std(scores))
    print("CLEAN MEAN:", scipy.mean(cleanScores), "MEDIAN:", scipy.median(cleanScores),
              "STD:", scipy.std(cleanScores))
    sys.stdout.flush()

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
