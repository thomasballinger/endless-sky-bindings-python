import shutil

import os
# homebrew installs here
assert os.path.exists('/usr/local/opt/jpeg-turbo/lib'), 'brew install jpeg-turbo'
assert os.path.exists('/usr/local/opt/jpeg-turbo/include')
shutil.copy('/usr/local/opt/jpeg-turbo/lib/libjpeg.dylib', 'endless_sky/lib/libjpeg.dylib')
shutil.copy('/usr/local/opt/jpeg-turbo/include/jpeglib.h', 'endless_sky/include/jpeglib.h')

