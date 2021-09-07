"""
Context managers for creating loading filesystems for Endless Sky code.
"""

import os
from contextlib import contextmanager
from pathlib import Path
from tempfile import TemporaryDirectory

from . import bindings as es

@contextmanager
def LoadedStringData(s, *, resources_path=None, config_path=None):
    with TemporaryDirectory() as tmpdir:
        tmpfile = os.path.join(tmpdir, 'mydata.txt')
        with open(tmpfile, 'w') as f:
            f.write(s)
        with LoadedData(tmpfile, resources_path=resources_path, config_path=config_path) as es:
            yield es

@contextmanager
def LoadedData(path, *, resources_path=None, config_path=None):
    """
    Load a file or folder of files, along with all data files in
    resources, global plugins (the plugins folder in resources), and
    local plugins (the plugins folder in config).

    Unless the files are already in the config path specified, the file
    or directory is temporarily symlinked in it with the name zzzTemp.
    Hopefully this name places this data last in the load order.

    resources_path defaults to a temporary, empty (but valid) resources directory.
    config_path defaults to a temporary, tempty (but valid) config directory.
    """

    if not os.path.exists(path):
        raise ValueError("Can't find the path "+repr(path))

    if resources_path is None:
        raise ValueError("not specifying a resources path is not yet tested")
    elif not os.path.exists(resources_path):
        raise ValueError("Nonexistent resource path "+repr(resources_path))

    if config_path is None:
        pass
    else:
        raise ValueError("specifying a config path is not yet tested")
        if os.path.exists(config_path):
            raise ValueError("Nonexistent resource path "+repr(resources_path))

    # TODO check that the path is not in the resources/data, images, or sounds
    # TODO check that path is not in the specified global plugins folder
    # TODO check if the path is not in the specified local plugins folder

    with ResourcesDir(resources_path) as resources:
        with ConfigDir(None) as config:
            config.link_plugin(path)
            es.GameData.BeginLoad(['foo', '--resources', resources.name, '--config', config.name])
            yield es

class ResourcesDir:
    def __init__(self, path=None):
        if path is None:
            raise ValueError("TempResourcesDir without an existing path is not tested")
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
        self.credits_path = os.path.join(path, 'credits')

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
        if path is not None:
            raise ValueError("TempConfig with an existing path is not tested")
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
        self.saves_path = os.path.join(self.tempdir.name, 'saves')
        self.plugins_path = os.path.join(self.tempdir.name, 'plugins')
        self.temp_plugin_path = os.path.join(self.plugins_path, 'zzzTemp')
        self.temp_plugin_data_path = os.path.join(self.plugins_path, 'zzzTemp', 'data')
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
                    os.path.remove(path)

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
