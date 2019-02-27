import subprocess
import sys
from runsecurify import *

maxIssues = int(sys.argv[1])
contract = sys.argv[2]

with open("run.txt", 'w') as outf:
    r = runSecurify(contract)
    if r > maxIssues:
        sys.exit(1)
    else:
        sys.exit(0)
