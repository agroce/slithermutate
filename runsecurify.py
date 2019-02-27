import subprocess
import os

def runSecurify(file):
    count = 0
    with open("out.txt", 'w') as outf:
        r = subprocess.call(["java", "-jar", os.getenv("SECURIFY_JAR"), "-fs", file],
                                stdout=outf, stderr=outf)
    with open("out.txt", 'r') as outf:
        for line in outf:
            if "Violation" in line:
                count += 1
    return count