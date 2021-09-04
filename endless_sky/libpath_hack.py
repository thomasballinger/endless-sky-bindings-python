import os
import sys
import platform

extra_dll_dir = os.path.join(os.path.dirname(__file__), 'lib')

print('considering libpath hack...')
if platform.system() == 'Windows':
    if sys.version_info >= (3, 8):
        os.add_dll_directory(extra_dll_dir)
        print('called add_dll_directory on', extra_dll_dir)
        print("in that dir:", os.listdir(extra_dll_dir))
        print("above that:", os.listdir(os.path.dirname(__file__)))
        print("and above that:", os.listdir(os.path.dirname(os.path.dirname(__file__))))
    else:
        # legacy DLL loading mechanism through PATH env variable manipulations
        os.environ.setdefault("PATH", "")
        os.environ["PATH"] += os.pathsep + extra_dll_dir
