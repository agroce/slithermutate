import subprocess
import sys
import os

experiments = [
    '''analyze_mutants mintoken4.sol "python runtimeout.py mintoken4.sol seq100.yaml TIMEOUT1" --mutantDir mutants6 --prefix EXPN.seq100.echidna --fromFile interesting_mutants.txt --timeout TIMEOUT2  >& EXPN.seq100.echidna.out''',
    '''analyze_mutants mintoken4.sol "python runtimeout.py mintoken4.sol seq200.yaml TIMEOUT1" --mutantDir mutants6 --prefix EXPN.seq200.echidna --fromFile interesting_mutants.txt --timeout TIMEOUT2  >& EXPN.seq200.echidna.out''',
    '''analyze_mutants mintoken4.sol "python runtimeout.py mintoken4.sol seq50.yaml TIMEOUT1" --mutantDir mutants6 --prefix EXPN.seq50.echidna --fromFile interesting_mutants.txt --timeout TIMEOUT2  >& EXPN.seq50.echidna.out''',        
    '''analyze_mutants mintoken4.sol "python runtimeout.py mintoken4.sol seq100nocov.yaml TIMEOUT1" --mutantDir mutants6 --prefix EXPN.seq100nocov.echidna --fromFile interesting_mutants.txt --timeout TIMEOUT2 >& EXPN.seq100nocov.echidna.out''',
    '''analyze_mutants mintoken4.sol "python runtimeout.py mintoken4.sol seq200nocov.yaml TIMEOUT1" --mutantDir mutants6 --prefix EXPN.seq200nocov.echidna --fromFile interesting_mutants.txt --timeout TIMEOUT2 >& EXPN.seq200nocov.echidna.out''',
    '''analyze_mutants mintoken4.sol "python runtimeout.py mintoken4.sol seq50nocov.yaml TIMEOUT1" --mutantDir mutants6 --prefix EXPN.seq50nocov.echidna --fromFile interesting_mutants.txt --timeout TIMEOUT2 >& EXPN.seq50nocov.echidna.out''',         
    '''analyze_mutants mintoken4.sol "python runtimeout.py mintoken4.sol seq10.yaml TIMEOUT1" --mutantDir mutants6 --prefix EXPN.seq10.echidna --fromFile interesting_mutants.txt --timeout TIMEOUT2 >& EXPN.seq10.echidna.out'''
    ]

timeout1 = sys.argv[1]
timeout2 = str(int(float(timeout1)*1.5))
print "RUNNING WITH TIMEOUTS", timeout1, timeout2

def fixTimeout(str):
    return (str.replace("TIMEOUT1", timeout1).replace("TIMEOUT2", timeout2))

experiments = map(fixTimeout, experiments)

for i in range(0,15):
    print "RUNNING", i
    for e in experiments:
        cmd = e.replace("EXPN", str(i))
        target = cmd.split(">& ")[1]
        if os.path.exists(target):
            print target, "ALREADY COMPLETED"
            continue
        subprocess.call([cmd], shell=True)
        
