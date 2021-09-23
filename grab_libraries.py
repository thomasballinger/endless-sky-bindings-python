#!/usr/bin/env python3
import shutil
import platform
from distutils.dir_util import copy_tree
from subprocess import check_call, check_output
import os

def list_files(startpath):
    print(os.path.abspath(startpath))
    if not os.path.exists(startpath):
        print('...does not exist')
        return
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print('{0}{1}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print('{0}{1}'.format(subindent, f))

shutil.rmtree('endless_sky/include', ignore_errors=True)
shutil.rmtree('endless_sky/lib', ignore_errors=True)

if platform.system() == 'Darwin':
    os.makedirs('endless_sky/include')
    os.makedirs('endless_sky/lib')

    # homebrew installs here
    assert os.path.exists('/usr/local/opt/jpeg-turbo'), 'brew install jpeg-turbo'
    shutil.copy('/usr/local/opt/jpeg-turbo/lib/libjpeg.dylib', 'endless_sky/lib/')
    copy_tree('/usr/local/opt/jpeg-turbo/include/', 'endless_sky/include/')
    # .dylib files contain metadata stating where they ought to be found!
    check_call(['install_name_tool', '-id', '@loader_path/lib/libjpeg.dylib', 'endless_sky/lib/libjpeg.dylib'])

    assert os.path.exists('/usr/local/opt/openal-soft'), 'brew install openal-soft'
    shutil.copy('/usr/local/opt/openal-soft/lib/libopenal.dylib', 'endless_sky/lib/')
    copy_tree('/usr/local/opt/openal-soft/include/', 'endless_sky/include/')
    check_call(['install_name_tool', '-id', '@loader_path/lib/libopenal.dylib', 'endless_sky/lib/libopenal.dylib'])

elif platform.system() == 'Linux':
    #assert False, "don't know how to harvest linux libs yet"
    list_files('/usr/local/lib')
    list_files('/usr/local/lib64')
    list_files('/usr/lib')
    list_files('/usr/lib64')
    #shutil.copy('/usr/local/opt/jpeg-turbo/lib/libjpeg.dylib', 'endless_sky/lib/')

    # statically linked:
    # gcc-c++

    # SDL2-devel
    # libpng-devel
    # libjpeg-turbo-devel
    # mesa-libGL-devel
    # glew-devel
    # openal-soft-devel
    # libmad-devel
    # libuuid-devel


elif platform.system() == 'Windows':
    assert os.path.exists('dev64'), "download MCO's Windows dev dependencies from https://endless-sky.github.io/win64-dev.zip"
    os.makedirs('endless_sky/include')
    os.makedirs('endless_sky/lib')

    # trust the bundle at https://endless-sky.github.io/win64-dev.zip
    copy_tree('dev64/include', 'endless_sky/include')
    copy_tree('dev64/bin', 'endless_sky/lib') # *.dll
    copy_tree('dev64/lib', 'endless_sky/lib') # *.dll.a  # TODO should these be copied over?
    DIR_MINGW64 = os.environ.get('DIR_MINGW64')
    assert DIR_MINGW64, "DIR_MINGW64 envar required"
    assert os.path.exists(DIR_MINGW64), "Need mingw installation at" + DIR_MINGW64
    shutil.copy(os.path.join(DIR_MINGW64, 'lib\libgcc_s_seh-1.dll'), 'endless_sky/lib/')
    shutil.copy(os.path.join(DIR_MINGW64, 'lib\libstdc++-6.dll'), 'endless_sky/lib/')
    shutil.copy(os.path.join(DIR_MINGW64, 'lib\libwinpthread-1.dll'), 'endless_sky/lib/')

else:
    assert False, "Platform not supported"

list_files('endless_sky/lib')
list_files('endless_sky/include')
