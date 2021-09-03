import shutil
from distutils.dir_util import copy_tree
import os

# This only runs on mac for now

shutil.rmtree('endless_sky/include', ignore_errors=True)
os.makedirs('endless_sky/include')
shutil.rmtree('endless_sky/lib', ignore_errors=True)
os.makedirs('endless_sky/lib')

# homebrew installs here
assert os.path.exists('/usr/local/opt/jpeg-turbo'), 'brew install jpeg-turbo'
shutil.copy('/usr/local/opt/jpeg-turbo/lib/libjpeg.dylib', 'endless_sky/lib/')
copy_tree('/usr/local/opt/jpeg-turbo/include/', 'endless_sky/include/')

assert os.path.exists('/usr/local/opt/openal-soft'), 'brew install openal-soft'
shutil.copy('/usr/local/opt/openal-soft/lib/libopenal.dylib', 'endless_sky/lib/')
copy_tree('/usr/local/opt/openal-soft/include/', 'endless_sky/include/')
