import sys
import time
import threading
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

pid = os.getpid()

def die_after_30s():
    """Force quit after a timeout"""
    time.sleep(30)
    subprocess.call(['Taskkill', '/PID', str(pid), '/F'])

t = threading.Thread(target=die_after_30s, daemon=True)
t.start()

# Python hangs here!
os._exit(0)
