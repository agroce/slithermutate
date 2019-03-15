from __future__ import print_function
import subprocess
import scipy
import scipy.stats

securify_issues = {}
securify_score = {}
slither_issues = {}
slither_score = {}
loc = {}
smartcheck_issues = {}
smartcheck_score = {}

def mutno(mutant):
    return int(mutant.split(".mutant.")[1].split(".")[0])

with open("stats_424_securify.txt", 'r') as securify_stats:
    for line in securify_stats:
        if "analyzing 424contracts/" in line:
            contract = line.split()[1]
        if "ISSUES:" in line:
            securify_issues[contract] = int(line.split()[-1])
        if "MUTATION SCORE" in line:
            securify_score[contract] = float(line.split()[-1])
        if "NO VALID MUTANTS" in line:
            securify_score[contract] = -1.0

with open("stats_424_slither.txt", 'r') as slither_stats:
    for line in slither_stats:
        if "analyzing 424contracts/" in line:
            contract = line.split()[1]
        if "ISSUES:" in line:
            slither_issues[contract] = int(line.split()[-1])
        if "LOC:" in line:
            loc[contract] = int(line.split()[-1])
        if "MUTATION SCORE" in line:
            slither_score[contract] = float(line.split()[-1])
        if "NO VALID MUTANTS" in line:
            slither_score[contract] = -1.0

with open("stats_424_smartcheck.txt", 'r') as smartcheck_stats:
    for line in smartcheck_stats:
        if "analyzing 424contracts/" in line:
            contract = line.split()[1]
        if "ISSUES:" in line:
            smartcheck_issues[contract] = int(line.split()[-1])
        if "MUTATION SCORE" in line:
            smartcheck_score[contract] = float(line.split()[-1])
        if "NO VALID MUTANTS" in line:
            smartcheck_score[contract] = -1.0

allClean = []
            
for contract in slither_score:
    print("="*80)
    print(contract)
    print ("ISSUE COUNTS: SLITHER", slither_issues[contract],
               "SECURIFY", securify_issues[contract],
               "SMARTCHECK", smartcheck_issues[contract])
    if (securify_issues[contract] == 0) and (slither_issues[contract] == 0) and (smartcheck_issues[contract] == 0):
        print("   -- ALL TOOLS FIND NO ISSUES --")
        if slither_score[contract] != -1.0:
            allClean.append(contract)
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
                subprocess.call(["diff", "424mutants/" + m, contract],
                                    stdout=diff_f, stderr=diff_f)
            with open("diffout.txt", 'r') as diff_f:
                for line in diff_f:
                    print(line, end="")
            print()
            any_smartcheck = True
        else:
            shared_kills.append(m)
    if any_smartcheck:
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

print()
print("+"*80)
print("ISSUES SUMMARY:")
print()
toolIssues = {}
for (tool, scores, issues) in [("slither", slither_score, slither_issues),
                       ("smartcheck", smartcheck_score, smartcheck_issues),
                       ("securify", securify_score, securify_issues)]:
    cbasis = filter(lambda x: scores[x] >= 0.0, scores.keys())
    svals = map(lambda x: issues[x], cbasis)
    toolIssues[tool] = svals
    print(tool, "MEAN:", scipy.mean(svals), "MEDIAN:", scipy.median(svals),
              "STD:", scipy.std(svals))
    print()
print()
print("STATISTICAL COMPARISONS:")
done = []
for tool1 in ["slither", "smartcheck", "securify"]:
    for tool2 in ["slither", "smartcheck", "securify"]:
        if tool1 == tool2:
            continue
        if sorted([tool1, tool2]) not in done:
            done.append(sorted([tool1, tool2]))
        else:
            continue
        print(tool1, "VS.", tool2 + ":")
        print(scipy.stats.wilcoxon(toolIssues[tool1], toolIssues[tool2]))
    
    
print()
print("+"*80)
print("MUTATION SCORE SUMMARY:")
print()
print(len(allClean), "CONTRACTS ARE CLEAN FOR ALL TOOLS")
toolScores = {}
toolCleanScores = {}
for (tool, scores) in [("slither", slither_score),
                       ("smartcheck", smartcheck_score),
                       ("securify", securify_score)]:
    svals = filter(lambda x: x >= 0.0, scores.values())
    toolScores[tool] = svals
    print(tool, "MEAN:", scipy.mean(svals), "MEDIAN:", scipy.median(svals),
              "STD:", scipy.std(svals))
    svals = map(lambda x: scores[x], allClean)
    toolCleanScores[tool] = svals
    print(tool, "CLEAN MEAN:", scipy.mean(svals), "MEDIAN:", scipy.median(svals),
              "STD:", scipy.std(svals))
    print()
print()
print("STATISTICAL COMPARISONS:")
done = []
for tool1 in ["slither", "smartcheck", "securify"]:
    for tool2 in ["slither", "smartcheck", "securify"]:
        if tool1 == tool2:
            continue
        if sorted([tool1, tool2]) not in done:
            done.append(sorted([tool1, tool2]))
        else:
            continue
        print(tool1, "VS.", tool2 + ":")
        print(scipy.stats.wilcoxon(toolScores[tool1], toolScores[tool2]))
        print("CLEAN:", scipy.stats.wilcoxon(toolCleanScores[tool1], toolCleanScores[tool2]))
