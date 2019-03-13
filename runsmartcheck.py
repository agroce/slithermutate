import subprocess
import os

def runSmartcheck(file):
    count = 0
    with open("smartout.txt", 'w') as outf:
        r = subprocess.call(["smartcheck", "-p", file],
                                stdout=outf, stderr=outf)
    with open("smartout.txt", 'r') as outf:
        for line in outf:
            if "severity: " in line:
                sev = int(line.split()[-1])
                if sev > 1:
                    count += 1
    return count
