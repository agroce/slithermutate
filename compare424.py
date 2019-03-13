from __future__ import print_function
import subprocess

securify_issues = {}
securify_score = {}
slither_issues = {}
slither_score = {}
smartcheck_issues = {}
smartcheck_score = {}

def mutno(mutant):
    return int(mutant.split(".mutant.")[1].split(".")[0])

with open("stats_424_securify.txt", 'r') as securify_stats:
    for line in securify_stats:
        if "analyzing contracts/" in line:
            contract = line.split()[1]
        if "ISSUES:" in line:
            securify_issues[contract] = int(line.split()[-1])
        if "MUTATION SCORE" in line:
            securify_score[contract] = float(line.split()[-1])
        if "NO VALID MUTANTS" in line:
            securify_score[contract] = -1.0

with open("stats_424_slither.txt", 'r') as slither_stats:
    for line in slither_stats:
        if "analyzing contracts/" in line:
            contract = line.split()[1]
        if "ISSUES:" in line:
            slither_issues[contract] = int(line.split()[-1])
        if "MUTATION SCORE" in line:
            slither_score[contract] = float(line.split()[-1])
        if "NO VALID MUTANTS" in line:
            slither_score[contract] = -1.0

with open("stats_424_smartcheck.txt", 'r') as smartcheck_stats:
    for line in smartcheck_stats:
        if "analyzing contracts424/" in line:
            contract = line.split()[1]
        if "ISSUES:" in line:
            smartcheck_issues[contract] = int(line.split()[-1])
        if "MUTATION SCORE" in line:
            smartcheck_score[contract] = float(line.split()[-1])
        if "NO VALID MUTANTS" in line:
            smartcheck_score[contract] = -1.0

for contract in slither_score:
    print("="*80)
    print(contract)
    print ("ISSUE COUNTS: SLITHER", slither_issues[contract],
               "SECURIFY", securify_issues[contract],
               "SMARTCHECK", smartcheck_issues[contract])
    if (securify_issues[contract] == 0) and (slither_issues[contract] == 0) and (smartcheck_issues[contract] == 0):
        print("   -- ALL TOOLS FIND NO ISSUES --")
    if slither_score[contract] == -1.0:
        print("NO VALID MUTANTS FOR THIS CONTRACT")
        print()
        print()
        continue
    print("MUTATION SCORES: SLITHER", slither_score[contract],
            "SECURIFY", securify_score[contract],
            "SMARTCHECK", smartcheck_score[contract])
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
    smartcheck_kills = []
    with open(contract.replace(".sol",".sol.smartcheck.killed.txt"), 'r') as smartcheck_killf:
        for line in smartcheck_killf:
            smartcheck_kills.append(line[:-1])
    shared_kills = []
    any_securify = False
    for m in sorted(securify_kills, key=mutno):
        if m not in slither_kills:
            print("securify detects", m, "not detected by slither")
            print("DIFF:")
            with open("diffout.txt", 'w') as diff_f:
                subprocess.call(["diff", "424mutants/" + m, contract],
                                    stdout=diff_f, stderr=diff_f)
            with open("diffout.txt", 'r') as diff_f:
                for line in diff_f:
                    print(line, end="")
            print()
            any_securify = True
        else:
            if m in smartcheck_kills:
                shared_kills.append(m)
    if any_securify:
        print()
    any_smartcheck = False
    for m in sorted(smartcheck_kills, key=mutno):
        if m not in slither_kills:
            print("smartcheck detects", m, "not detected by slither")
            if m in securify_kills:
                print("** mutant detected by both non-slither tools **")
            print("DIFF:")
            with open("diffout.txt", 'w') as diff_f:
                subprocess.call(["diff", "mutants/" + m, contract],
                                    stdout=diff_f, stderr=diff_f)
            with open("diffout.txt", 'r') as diff_f:
                for line in diff_f:
                    print(line, end="")
            print()
            any_smartcheck = True
        else:
            shared_kills.append(m)
    if any_securify:
        print()
    any_slither = False
    for m in sorted(slither_kills, key=mutno):
        if m not in securify_kills:
            print("slither detects", m, "not detected by securify")
            any_slither = True
        if m not in smartcheck_kills:
            print("slither detects", m, "not detected by smartcheck")
            any_slither = True            
    if any_slither:
        print()
    if len(shared_kills) > 0:
        print(len(shared_kills), "MUTANTS WERE DETECTED BY ALL TOOLS:")
        for m in shared_kills:
            print("  ", m)
    print()
    
