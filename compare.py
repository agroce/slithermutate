from __future__ import print_function
import subprocess

securify_issues = {}
securify_score = {}
slither_issues = {}
slither_score = {}

with open("stats_securify.txt", 'r') as securify_stats:
    for line in securify_stats:
        if "analyzing contracts/" in line:
            contract = line.split()[1]
        if "ISSUES:" in line:
            securify_issues[contract] = int(line.split()[-1])
        if "MUTATION SCORE" in line:
            securify_score[contract] = float(line.split()[-1])
        if "NO VALID MUTANTS" in line:
            securify_score[contract] = -1.0

with open("stats_slither.txt", 'r') as slither_stats:
    for line in slither_stats:
        if "analyzing contracts/" in line:
            contract = line.split()[1]
        if "ISSUES:" in line:
            slither_issues[contract] = int(line.split()[-1])
        if "MUTATION SCORE" in line:
            slither_score[contract] = float(line.split()[-1])
        if "NO VALID MUTANTS" in line:
            slither_score[contract] = -1.0

for contract in slither_score:
    print("="*80)
    print(contract)
    if slither_issues[contract] > securify_issues[contract]:
        print("SLITHER FINDS MORE ISSUES IN ORIGINAL")
    if securify_issues[contract] > slither_issues[contract]:
        print("SECURIFY FINDS MORE ISSUES IN ORIGINAL")
    if (securify_issues[contract] == 0) and (slither_issues[contract] == 0):
        print("BOTH TOOLS FIND NO ISSUES")
    if (slither_score[contract] == -1.0) and (securify_score[contract] == -1.0):
        print("NO VALID MUTANTS FOR THIS CONTRACT")
        print()
        print()
        continue
    print("*"*40)
    print()
    slither_kills = []
    with open(contract.replace(".sol",".sol.slither.killed.txt"), 'r') as slither_killf:
        for line in slither_killf:
            slither_kills.append(line[:-1])
    securify_kills = []
    with open(contract.replace(".sol",".sol.securify.killed.txt"), 'r') as securify_killf:
        for line in securify_killf:
            securify_kills.append(line[:-1])
    shared_kills = []
    any_securify = False
    for m in securify_kills:
        if m not in slither_kills:
            print("securify detects", m, "not detected by slither")
            any_securify = True
        else:
            shared_kills.append(m)
    if any_securify:
        print()
    any_slither = False
    for m in slither_kills:
        if m not in securify_kills:
            print("slither detects", m, "not detected by securify")
            any_slither = True
    if any_slither:
        print()
    print(len(shared_kills), "MUTANTS WERE DETECTED BY BOTH TOOLS")
    print()
    print()
        
    
