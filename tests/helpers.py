import os
import subprocess

import pytest

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

@pytest.fixture
def empty_resources_dir(tmp_path):
    r = tmp_path / "resources"
    r.mkdir()
    data = r / "data"; data.mkdir()
    images = r / "images"; images.mkdir()
    sounds = r / "sounds"; sounds.mkdir()
    p = r / "credits.txt"
    p.write_text("some awesome folks\n")
    return r

@pytest.fixture
def empty_config_dir(tmp_path):
    r = tmp_path / "config"
    r.mkdir()
    saves = r / "saves"
    saves.mkdir()
    saves = r / "plugins"
    saves.mkdir()
    return r
