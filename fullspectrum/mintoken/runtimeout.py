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
    
echidna_cmd = echidna + " " + sol + " --config " + config + " >& " + echidna_out


P = subprocess.Popen([echidna_cmd], shell=True, preexec_fn=os.setsid)
pgrp = os.getpgid(P.pid)
foundFailure = False
start = time.time()
while ((time.time() - start) < timeout) and (not foundFailure) and (P.poll() is None):
    if os.path.exists(echidna_out):
        with open(echidna_out, 'r') as currentResults:
            for line in currentResults:
                if ": failed" in line:
                    foundFailure = True
                    break
    time.sleep(0.25)

os.killpg(pgrp, signal.SIGKILL)
subprocess.call(["mv " + echidna_out + " echidna.out"], shell=True)

if foundFailure:
    print("FAILED!")
    sys.exit(1)
else:
    print("TIMED OUT OR TERMINATED")


    
sys.exit(0)
