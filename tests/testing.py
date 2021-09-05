import sys
import time
import subprocess

print("running tests/testing.py")
sys.stdout.flush()


print("importing endless_sky.bindings")
sys.stdout.flush()

import endless_sky.bindings as m

print("imported")
sys.stdout.flush()

import os

def test_Point():
    p = m.Point(1, 2)
    assert p.X == 1
    assert p.Y == 2

test_Point()

print("ran code")
sys.stdout.flush()

print("now let's try to exit")
sys.stdout.flush()

## this works if necessary
#subprocess.call(['Taskkill', '/PID', str(os.getpid()), '/F'])

# Python hangs here!
os._exit(0)  # this is the strongest quit I know how to do (doesn't propagate
             # exceptions or run atexits) but it's not enough!
