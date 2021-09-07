import os
import sys
import platform

extra_dll_dir = os.path.join(os.path.dirname(__file__), 'lib')

if platform.system() == 'Windows':
    if sys.version_info >= (3, 8):
        os.add_dll_directory(extra_dll_dir)
    else:
        # legacy DLL loading mechanism through PATH env variable manipulations
        os.environ.setdefault("PATH", "")
        os.environ["PATH"] += os.pathsep + extra_dll_dir
