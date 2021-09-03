import shutil
import platform
from distutils.dir_util import copy_tree
import os

def list_files(startpath):
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print('{}{}'.format(subindent, f))

shutil.rmtree('endless_sky/include', ignore_errors=True)
shutil.rmtree('endless_sky/lib', ignore_errors=True)

if platform.system() == 'Darwin':
    os.makedirs('endless_sky/include')
    os.makedirs('endless_sky/lib')

    # homebrew installs here
    assert os.path.exists('/usr/local/opt/jpeg-turbo'), 'brew install jpeg-turbo'
    shutil.copy('/usr/local/opt/jpeg-turbo/lib/libjpeg.dylib', 'endless_sky/lib/')
    copy_tree('/usr/local/opt/jpeg-turbo/include/', 'endless_sky/include/')

    assert os.path.exists('/usr/local/opt/openal-soft'), 'brew install openal-soft'
    shutil.copy('/usr/local/opt/openal-soft/lib/libopenal.dylib', 'endless_sky/lib/')
    copy_tree('/usr/local/opt/openal-soft/include/', 'endless_sky/include/')

elif platform.system() == 'Linux':
    assert False, "don't know how to harvest linux libs yet"

elif platform.system() == 'Windows':
    assert os.path.exists('dev64'), "download MCO's Windows dev dependencies from https://endless-sky.github.io/win64-dev.zip"
    os.makedirs('endless_sky/include')
    os.makedirs('endless_sky/lib')

    # trust the bundle at https://endless-sky.github.io/win64-dev.zip
    copy_tree('dev64/include', 'endless_sky/include')
    copy_tree('dev64/bin', 'endless_sky/lib')
    copy_tree('dev64/lib', 'endless_sky/lib')

else:
    assert False, "Platform not supported"

list_files('endless_sky/lib')
list_files('endless_sky/include')
