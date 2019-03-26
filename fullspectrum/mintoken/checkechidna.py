from __future__ import print_function
import subprocess
import sys

sol = sys.argv[1]
config = sys.argv[2]

with open("echidna.out", 'w') as echidnaf:
    subprocess.call(["echidna-test", sol, "--config", config],
                    stdout=echidnaf, stderr=echidnaf)

with open("echidna.out", 'r') as echidnaf:
    for line in echidnaf:
        print(line, end="")
        if "failed!" in line:
            sys.exit(1)

sys.exit(0)
