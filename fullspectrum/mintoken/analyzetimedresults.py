import glob
import scipy
import scipy.stats
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

def label(text):
    l = text.replace("seq","")
    if "nocov" in l:
        l = l.replace("nocov", "")
    else:
        l = l + "cov"
    return l

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

sortKeys = sorted(data.keys(), key=lambda c:scipy.mean(data[c]))
            
compared = []
for config in sortKeys:
    d = data[config]
    print "="*80
    print "SEQLEN", label(config), "RUNS:", len(d), "MEAN:", scipy.mean(d), "MEDIAN:", scipy.median(d), "STD:", scipy.std(d)
    if len(d) > 2:
        for config2 in sortKeys:
            if (config != config2) and (sorted([config, config2]) not in compared):
                P = scipy.stats.mannwhitneyu(d, data[config2]).pvalue
                #print ".vs", config2, round(P, 2),
                if P < 0.05:
                    print "STATISTICALLY WORSE THAN", label(config2), "P =",round(P, 3)
                compared.append(sorted([config, config2]))
    

f1 = plt.figure(figsize=(10,4))

plt.ylabel("Mutation score")
plt.xlabel("seqLen/coverage")

nameTuple = tuple(sortKeys)

#plt.xticks(xrange(0,len(nameTuple)), nameTuple)
plt.xticks(range(1,len(nameTuple)+1), map(label, sortKeys))

bb = plt.boxplot(map(lambda k: data[k], sortKeys), manage_xticks=False)

#bb = plt.boxplot([data["random"]["branch"],data["LOC"]["branch"],data["swarm"]["branch"],data["LOC+swarm"]["branch"],data["GA"]["branch"],data["LOC+GA"]["branch"]],manage_xticks=False)

pp = PdfPages("scores.pdf")

pp.savefig(f1)
pp.close()
