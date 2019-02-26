import subprocess
import glob
import sys

for C in glob.glob("*.sol"):
    if "mutant" in C:
        continue # don't analyze the mutants themselves!
    print "="*80
    print "analyzing", C
    with open("out.txt", 'w') as outf:
        num_base = subprocess.call(["slither", C, "--exclude-informational"], stdout=outf, stderr=outf)
    print "ISSUES:", num_base
    sys.stdout.flush()    
    with open("out.txt", 'w') as outf:
        r = subprocess.call(["mutate", C], stdout=outf, stderr=outf)
    with open("out.txt", 'r') as outf:
        for line in outf:
            if "MUTANTS" in line:
                print line,
    sys.stdout.flush()
    with open("out.txt", 'w') as outf:
        subprocess.call(["analyze_mutants", C, "python maxissues.py " + str(num_base) + " " + C],
                            stdout=outf, stderr=outf)
    with open("out.txt", 'r') as outf:
        for line in outf:
            if "MUTATION SCORE" in line:
                print line,
    subprocess.call(["wc","-l","killed.txt"])
    subprocess.call(["wc","-l","notkilled.txt"])
    sys.stdout.flush()    
    subprocess.call(["cp","killed.txt",C+".killed.txt"])
    subprocess.call(["cp","notkilled.txt",C+".notkilled.txt"])
