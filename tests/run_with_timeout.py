import time
import platform
import subprocess
import sys

process = subprocess.Popen(sys.argv[1:])

TIMEOUT = 45

try:
    process.wait(TIMEOUT)
except subprocess.TimeoutExpired:
    assert platform.system() == 'Windows', "should only time out on Windows!"
    # still alive, let's kill it
    print("Hit timeout, running Taskkill on", str(process.pid))
    sys.stdout.flush()
    subprocess.call(['Taskkill', '/PID', str(process.pid), '/F'])
    print("failed the 'can exit without hanging forever' test")
    sys.exit(1)
else:
    sys.exit(process.returncode)
