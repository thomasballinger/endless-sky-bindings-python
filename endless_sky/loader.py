"""
Context managers for creating loading filesystems for Endless Sky code.
"""

import os
import atexit
import logging
from pathlib import Path
from tempfile import TemporaryDirectory
from contextlib import contextmanager

from . import bindings as es

LOADED = False

class AlreadyLoadedError(Exception):
    """
    Endless Sky resources and plugins can only be loaded once.
    Restart Python to load a new set of plugins and resources.

    Endless Sky GameData is a singleton, and the bad kind. It has global
    (static class members in C++) state that can't even properly be reset.
    """

def load_string_data(s, *, resources=None, config=None):
    """Load data and wait to clean up temporary directories until Python exits"""
    context = LoadedStringData(s, resources=resources, config=config)
    es = context.__enter__()
    atexit.register(lambda: context.__exit__(None, None, None))
    return es

def load_data(path=None, *, resources=None, config=None):
    """Load data and wait to clean up temporary directories until Python exits"""
    context = LoadedData(path, resources=resources, config=config)
    es = context.__enter__()
    atexit.register(lambda: context.__exit__(None, None, None))
    return es

@contextmanager
def LoadedStringData(s, *, resources=None, config=None):
    with TemporaryDirectory() as tmpdir:
        tmpfile = os.path.join(tmpdir, 'mydata.txt')
        with open(tmpfile, 'w') as f:
            f.write(s)
        yield load_data(tmpfile, resources=resources, config=config)

#TODO something special with the errors.txt file in config - offer to send to stderr?

@contextmanager
def FilesystemPrepared(path=None, *, resources=None, config=None):
    """
    Ready the filesystem with path, resources, and config.
    """
    if path and not os.path.exists(path):
        raise ValueError("Can't find the path "+repr(path))

    if resources and not os.path.exists(resources):
        raise ValueError("Nonexistent resource path "+repr(resources))

    if config is not None and not os.path.exists(config):
        raise ValueError("Nonexistent config path "+repr(config))

    # TODO check that the path is not in the resources/data, images, or sounds
    # TODO check that path is not in the specified global plugins folder
    # TODO check if the path is not in the specified local plugins folder

    with ResourcesDir(resources) as r:
        with ConfigDir(config) as c:
            if path:
                c.link_plugin(path)
            yield (r.name, c.name)

@contextmanager
def LoadedData(path=None, *, resources=None, config=None):
    """
    Load a file or folder of files, data files in resources, global
    plugins (the plugins folder in resources), and local plugins
    (the plugins folder in config).

    Each of path, resources, and config is an optional path as a string.

    Returns a reference to the endless_sky.bindings module, but you can
    ignore this return value and import it directly instead if you want.

    Unless the files are already in the config path specified, the file
    or directory is temporarily symlinked in it with the name zzzTemp.
    Hopefully this name places this data last in the load order.

    resources defaults to a temporary, empty (but valid) resources directory.
    config defaults to a temporary, tempty (but valid) config directory.
    """
    global LOADED

    if LOADED:
        raise AlreadyLoadedError("Data already loaded, restart Python to load again.")

    with FilesystemPrepared(path=path, resources=resources, config=config) as (resources_path, config_path):
        args = ['foo', '--resources', resources_path, '--config', config_path]
        logging.warn('BeginLoad(%s)', args)
        try:
            es.GameData.BeginLoad(args)
        except RuntimeError as e:
            if 'Unable to find the resource directories' in str(e):
                print(args)
                print(r.name, os.listdir(r.name))
                print(c.name, os.listdir(c.name))
                raise
            else:
                raise
        LOADED = True
        yield es

class ResourcesDir:
    def __init__(self, path=None):
        self.path = path

    @property
    def name(self):
        return self.tempdir.name if self.temp else self.path

    @property
    def temp(self):
        return self.path is None

    def __enter__(self):
        if self.temp:
            self.tempdir = TemporaryDirectory()

        path = self.tempdir.name if self.temp else self.path
        self.data_path = os.path.join(path, 'data')
        self.images_path = os.path.join(path, 'images')
        self.sounds_path = os.path.join(path, 'sounds')
        self.credits_path = os.path.join(path, 'credits.txt')

        if self.temp:
            os.mkdir(self.data_path)
            os.mkdir(self.images_path)
            os.mkdir(self.sounds_path)
            Path(self.credits_path).touch()
        return self

    def __exit__(self, type, value, traceback):
        if self.temp:
            self.tempdir.cleanup()

class ConfigDir:
    def __init__(self, path=None):
        self.path = path
        self.to_remove = []
        self.plugin_linked = False

    @property
    def name(self):
        return self.tempdir.name if self.temp else self.path

    @property
    def temp(self):
        return self.path is None

    def __enter__(self):
        if self.temp:
            self.tempdir = TemporaryDirectory()

        path = self.tempdir.name if self.temp else self.path
        self.saves_path = os.path.join(self.name, 'saves')
        self.plugins_path = os.path.join(self.name, 'plugins')
        self.temp_plugin_path = os.path.join(self.plugins_path, 'zzzTemp')
        self.temp_plugin_data_path = os.path.join(self.plugins_path, 'zzzTemp', 'data')

        if self.temp:
            os.mkdir(self.saves_path)
            os.mkdir(self.plugins_path)
        return self

    def __exit__(self, type, value, traceback):
        if self.temp:
            self.tempdir.cleanup()
        else:
            for path in reversed(self.to_remove):
                if os.path.isdir(path):
                    os.rmdir(path)
                else:
                    os.remove(path)

    def link_plugin(self, path):
        """Symlink a path or create a folder and a symlink in that folder."""
        if self.plugin_linked:
            raise ValueError("Already linked a plugin")
        os.mkdir(self.temp_plugin_path)
        self.to_remove.append(self.temp_plugin_path)
        if os.path.isdir(path):
            os.symlink(os.path.abspath(path), self.temp_plugin_data_path, target_is_directory=True)
            self.to_remove.append(self.temp_plugin_data_path)
        else:
            os.mkdir(self.temp_plugin_data_path)
            self.to_remove.append(self.temp_plugin_data_path)
            symlink_path = os.path.join(self.temp_plugin_data_path, os.path.basename(path))
            os.symlink(os.path.abspath(path), symlink_path, target_is_directory=False)
            self.to_remove.append(symlink_path)
        self.plugin_linked = True
