import glob
import scipy
import scipy.stats

data = {}

for f in glob.glob("*.echidna.out"):
    numAndName = f.split(".echidna.out")[0]
    [num, name] = numAndName.split(".")
    score = None
    with open(f, 'r') as resultf:
        for line in resultf:
            if "MUTATION SCORE:" in line:
                score = float(line.split()[-1])
    if score is not None:
        if name not in data:
            data[name] = [score]
        else:
            data[name].append(score)

compared = []
for config in sorted(data.keys(), key=lambda c:scipy.mean(data[c])):
    d = data[config]
    print config, len(d), scipy.mean(d), scipy.median(d), scipy.std(d)
    if len(d) > 2:
        for config2 in sorted(data.keys(), key=lambda c:scipy.mean(data[c])):
            if (config != config2) and (sorted([config, config2]) not in compared):
                print ".vs", config2, scipy.stats.mannwhitneyu(d, data[config2])
                compared.append(sorted([config, config2]))
    
