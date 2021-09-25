import platform
import os
import logging
from pathlib import Path
from io import BytesIO
from urllib.request import urlopen
from zipfile import ZipFile

import platformdirs

from . import endless_sky_version

def download_and_extract_zipfile(zipurl, dir):
    with urlopen(zipurl) as zipresp:
        with ZipFile(BytesIO(zipresp.read())) as zfile:
            zfile.extractall(dir)

def cached_resources():
    data_dir = platformdirs.user_data_dir("EndlessSkyPython", False)
    cache_path = Path(os.path.join(data_dir, 'endless-sky-'+endless_sky_version))
    cache_path.mkdir(parents=True, exist_ok=True)

    if os.path.exists(cache_path / 'credits.txt'):
        logging.info("Using cached resources at", cache_path)
        return str(cache_path)

    github_url = "https://github.com/endless-sky/endless-sky/archive/"+endless_sky_version+".zip"
    logging.warning('No cached resources found for', endless_sky_version[:7])
    logging.warning('Downloading to %s', str(data_dir))
    logging.warning('this may take a minute...')
    download_and_extract_zipfile(github_url, data_dir)
    return str(cache_path)


def es2lancher_resources(instancesPath, resourcesPath):
  resources = [];
  instances = [];
  try:
    instances.extend(os.listdir(instancesPath))
  except FileNotFoundError:
      return []
  return [os.path.join(instancesPath, instance, resourcesPath)
          for instance in instances]

def find_resources():
    """Returns an already installed resource of Endless Sky, or throws ValueError"""
    candidates = []
    if platform.system() == "Darwin":
        candidates.append("/Applications/Endless Sky.app/Contents/Resources");
        eslauncher2 = os.path.expanduser(
          "~/Library/Application Support/ESLauncher2/instances/"
        )
        resources_path = "Endless Sky.app/Contents/Resources"
        candidates.extend(es2lancher_resources(eslauncher2, resources_path))
    elif platform == "Windows":
        # TODO add normal install location
        eslauncher2 = os.path.expanduser(
          "~/LocalAppData\\Roaming\\ESLauncher2\\instances"
        )
        resources_path = ""
        candidates.extend(es2lancher_resources(eslauncher2, resources_path))
    # TODO add Linux locations
    look_like_resources = [
        path for path in candidates
        if os.path.exists(os.path.join(path, 'credits.txt'))
        if os.path.exists(os.path.join(path, 'data'))
        if os.path.exists(os.path.join(path, 'images'))
        if os.path.exists(os.path.join(path, 'sounds'))
    ]
    if not look_like_resources:
        raise ValueError("Can't find a version of Endless Sky already installed.")
    use = look_like_resources[0]
    logging.warning('Using resources at %s', str(use))
    return use;
