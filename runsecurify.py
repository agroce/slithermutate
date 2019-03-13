import subprocess
import os

def runSecurify(file):
    count = 0
    with open("securifyout.txt", 'w') as outf:
        r = subprocess.call(["java", "-jar", os.getenv("SECURIFY_JAR"), "-fs", file],
                                stdout=outf, stderr=outf)
    with open("securifyout.txt", 'r') as outf:
        for line in outf:
            if "Violation" in line or "Warning" in line:
                count += 1
    return count
