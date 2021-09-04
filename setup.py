import platform
from setuptools import setup
from glob import glob
import os
import sys
import sysconfig

from pybind11.setup_helpers import Pybind11Extension, build_ext

# Monkey-patch PyBindExtension to convert \foo flags to -foo
# because it adds some \args on Windows assuming we're using compiler that likes that
def mvsc_to_mingw(flag):
    if flag == '/bigobj':
        return '-Wa,-mbig-obj'
    if flag == '/EHsc':
        return ''
    if flag == '/std:c++latest':
        return "-std=c++2a"
    if flag.startswith('/'):
        return ''
    return flag

def _add_cflags(self, flags):
    flags = [mvsc_to_mingw(flag) for flag in flags if mvsc_to_mingw(flag)]
    self.extra_compile_args[:0] = flags
Pybind11Extension._add_cflags = _add_cflags

# There are two different sdists builds possible.
# With ES_SETUP_INCLUDE_LIBRARIES set (eg when building wheels) we copy
# in all libraries into endless_sky/lib. This produces a build that only
# works on a single platform because we harvest the libraries from the system.
# Without ES_SETUP_INCLUDE_LIBRARIES set (eg when the package will be run on
# the very same machine that is building it) we do not copy these libraries in
# and just look for library folders on the OS.
INCLUDE_LIBRARIES = (os.environ.get('ES_SETUP_INCLUDE_LIBRARIES') or '0') == '1'
print('INCLUDE_LIBRARIES:', INCLUDE_LIBRARIES)

# A "real" source distribution might include the shared libraries for every platform.

# Once we have an sdist we use the presence of endless_sky/lib to determine
# whether to use the system lib locations or the local ones.
LIBRARIES_INCLUDED = os.path.exists('endless_sky/lib/')
print('LIBRARIES_INCLUDED:', LIBRARIES_INCLUDED)

if INCLUDE_LIBRARIES:
    assert LIBRARIES_INCLUDED, "can't include libraries if endless_sky/lib/ does not exist. Run ./grab_libraries.py to harvest libs from the OS."

# Endless Sky requires libraries like dirent.h that are not provided by MSVC,
# so mingw should be used when compiling on Windows.
# DIR_MINGW64 is defined in .github/workflows CI, pointing to the
# location of already-installed mingw in the GitHub Actions environment.
# To compile locally on Windows you'll need to set this.
# Don't do this, install the wheel instead.
DIR_MINGW64 = os.environ.get('DIR_MINGW64')

# https://stackoverflow.com/questions/63804883/including-and-distributing-third-party-libraries-with-a-python-c-extension
def path_to_build_folder():
    """Returns the name of a distutils build directory"""
    f = "{dirname}.{platform}-{version[0]}.{version[1]}"
    dir_name = f.format(dirname='lib',
                    platform=sysconfig.get_platform(),
                    version=sys.version_info)
    return os.path.join('build', dir_name, 'endless_sky')

# https://stackoverflow.com/a/57109148/398212
# TODO do we also need extra_link_args = ["-Wl,-Bstatic", "-lpthread"]
if platform.system() == "Windows":
    import distutils.cygwinccompiler
    # monkeypatch for too-recent MSVC versions
    distutils.cygwinccompiler.get_msvcr = lambda: []

# Update these with new releases
__version__ = "0.0.2"
endless_sky_version = "753db45e921b7b7d57bb7b4afaf5181acbe0a6cc"

# The initial goal here is to create a source distribution (sdist) that could
# be downloaded and installed on any platform.
# For this to be possible, dylib/so/DLL files for all platforms need to be
# included OR instructions about how to install them need to be included.
# To get things going, start by linking in jpegturbo and openal - but eventually
# these needn't be in the sdist, they should just be in the wheels.
# Windows DLLs will be included in the sdist, but mac and linux.
# Maybe libs will be included in wheels, but not in sdist? In that case
# we will need to separate setup() invocations in setup.py, one for wheels!
# That's probably the way to go.

# TODO use info at https://pybind11.readthedocs.io/en/stable/compiling.html
# to speed this compile process up when iterating.

def crash(msg=''):
    raise AssertionError((msg or 'TODO') + ' on platform ' + platform.system())

extra_compile_args=[
        '-Wno-deprecated-declarations', # ignore mac OpenGL deprecation warnings
        #'-v',  # for debugging an include
        #'-H',  # for debugging an include
        ] if platform.system() == "Darwin" else [
        #'-v',  # for debugging an include
        #'-H',  # for debugging an include
        ] if platform.system() == "Windows" else []

extra_link_args = (['-Wl,--verbose'] if platform.system() == "Windows" else [
    "-Wl,-rpath,$ORIGIN/lib/."
])

pybind_extension = Pybind11Extension("endless_sky.bindings", [
        "endless_sky/lib.cpp",
#        "endless_sky/endless-sky/tests/src/helpers/datanode-factory.cpp",
    ] + sorted(
        glob('endless_sky/endless-sky/source/Point.cpp') +
        glob('endless_sky/endless-sky/source/Random.cpp')
#        glob('endless_sky/endless-sky/source/*.cpp') +
#        glob('endless_sky/endless-sky/source/text/*.cpp')
    ),
    libraries=[
        "winmm",
        "mingw32",
#        "sdl2main",
#        "sdl2.dll",
#        "png.dll",
#        "turbojpeg.dll",
#        "jpeg.dll",
#        "openal32.dll",
        "rpcrt4",
#        "glew32.dll",
#        "opengl32",
#        'mad',
    ] if platform.system() == "Windows" else (
        [
            'jpeg',
            'SDL2',
            'png',
            'openal',
            'mad',
        ] + (
            [] if platform.system() == "Darwin" else [
                'uuid',
                'GL',
                'GLEW',
            ]
        )
    ),
    library_dirs=(
        [os.path.join(path_to_build_folder(), 'lib')] if LIBRARIES_INCLUDED else (
            [
                '/usr/local/opt/jpeg-turbo/lib',
                '/usr/local/opt/openal-soft/lib',
            ] if platform.system() == 'Darwin' else [
                #TODO does anything need to be manually included here?
                # Probably not, linux just works?
            ] if platform.system() == 'Linux' else [
                 './dev64/lib', # *.dll.a # TODO should these be included?
                 './dev64/bin', # *.dll
            ] if platform.system() == "Windows" else crash())),
    include_dirs=(
        ([os.path.join(path_to_build_folder(), 'include')] if LIBRARIES_INCLUDED else (
            [
                '/usr/local/opt/jpeg-turbo/include',
                '/usr/local/opt/openal-soft/include',
            ] if platform.system() == 'Darwin' else [
                #TODO does anything need to be manually included here?
                # Probably not, linux just works?
            ] if platform.system() == 'Linux' else [
                './dev64/include'
            ] if platform.system() == 'Windows' else crash())) + [
        os.path.join(path_to_build_folder(), 'endless-sky/tests/include'),
        os.path.join(path_to_build_folder(), 'endless-sky/endless-sky/source'),
        os.path.join(path_to_build_folder(), 'endless-sky/endless-sky/source/text'),
    ]),
    extra_compile_args=extra_compile_args,
    extra_link_args=extra_link_args,
    define_macros=[
            ('VERSION_INFO', __version__),
            ('ENDLESS_SKY_VERSION_INFO', endless_sky_version),
    ],
)

setup(
    name="endless-sky-bindings",  # I'd like to change this to endless-sky but 
    version=__version__,          # want to prove out the library before doing that
    author="Thomas Ballinger",
    author_email="thomasballinger@gmail.com",
    url="https://github.com/thomasballinger/endless-sky-bindings-python",
    description="Python bindings for Endless Sky C++ code",
    long_description="",
    ext_modules = [pybind_extension],
    packages=['endless_sky'],
    package_data={
        'endless_sky': [
            'endless-sky/tests/include/*.h',
            'endless-sky/tests/include/*.hpp',
            'endless-sky/source/*.h',
            'endless-sky/source/*.hpp',
            'endless-sky/source/text/*.h',
            'endless-sky/source/text/*.hpp',
        ] + ([
            'include/*.h',
            'include/*/*.h',
            'lib/*',
        ] if INCLUDE_LIBRARIES else [])
    },
    extras_require={"test": "pytest"},
    # Currently, build_ext only provides an optional "highest supported C++
    # level" feature, but in the future it may provide more features.
    cmdclass={"build_ext": build_ext},
    zip_safe=False,
)

"""
    data_files=([  # TODO - THIS IS NOT A THING!
        (
            '', # install in the package folder
            sorted(glob(".\dev64\bin\*.dll")) + [
                DIR_MINGW64 + "\lib\libgcc_s_seh-1.dll",
                DIR_MINGW64 + "\lib\libstdc++-6.dll",
                DIR_MINGW64 + "\lib\libwinpthread-1.dll",
            ]
        )
    ] if platform.system() == "Windows" and DIR_MINGW64 else [])
"""
