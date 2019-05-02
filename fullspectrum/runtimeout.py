from __future__ import print_function
import subprocess
import sys
import time
import os
import signal

sol = sys.argv[1]
config = sys.argv[2]
timeout = int(sys.argv[3])

echidna = "echidna-test"
if "--master" in sys.argv:
    echidna = "echidna-master"

echidna_out = "echidna.out." + str(os.getpid())
    
echidna_cmd = echidna + " " + sol + " TEST --config " + config + " >& " + echidna_out

P = subprocess.Popen([echidna_cmd], shell=True, preexec_fn=os.setsid)
pgrp = os.getpgid(P.pid)
foundFailure = False
start = time.time()
lastReport = 0
INTERVAL = 60
try:
    while ((time.time() - start) < timeout) and (not foundFailure) and (P.poll() is None):
        if ((int(time.time() - start) % INTERVAL) == 0) and (lastReport != int(time.time()-start)):
            print(int(time.time() - start), "SECONDS ELAPSED...", end=" ")
            sys.stdout.flush()
            lastReport = int(time.time() - start)
        if os.path.exists(echidna_out):
            with open(echidna_out, 'r') as currentResults:
                for line in currentResults:
                    if ": failed" in line:
                        failureText = ""
                        toSplit = line
                        while ": failed" in toSplit:
                            failSplit = toSplit.split(": failed", 1)
                            failureText += failSplit[0].split()[-1] + ": failed!  "
                            toSplit = failSplit[1]
                        foundFailure = True
                        break
        if not foundFailure:
            time.sleep(0.25)
finally:
    os.killpg(pgrp, signal.SIGTERM)
    subprocess.call(["mv " + echidna_out + " echidna.out"], shell=True)

if lastReport != 0:
    print()

if foundFailure:
    print("FAILED IN", time.time() - start, "SECONDS:")
    print(failureText)
    sys.exit(1)
else:
    print("TIMED OUT OR TERMINATED")
    
sys.exit(0)
