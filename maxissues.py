import subprocess
import sys

maxIssues = int(sys.argv[1])
contract = sys.argv[2]

with open("run.txt", 'w') as outf:
    r = subprocess.call(["slither", contract, "--exclude-informational"], stdout=outf, stderr=outf)
    if r > maxIssues:
        sys.exit(1)
    else:
        sys.exit(0)
