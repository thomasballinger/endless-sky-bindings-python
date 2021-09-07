import os
import subprocess

if os.environ.get("THIS_IS_THE_SUBPROCESS"):
    def icky_global_state(func):
        return func
else:
    def icky_global_state(func):
        def run_in_subprocess():
            specifier = f"{func.__globals__['__file__']}::{func.__name__}"
            print('isolated test: running pytest on', specifier)
            subprocess.check_call(['pytest', specifier], env=dict(os.environ, THIS_IS_THE_SUBPROCESS="1"))
        run_in_subprocess.__name__ = func.__name__
        return run_in_subprocess
