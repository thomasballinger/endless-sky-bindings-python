import platform
from setuptools import setup
from glob import glob
import os
import sys
import sysconfig

from pybind11.setup_helpers import Pybind11Extension, build_ext

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

if platform.system() == "Windows" and DIR_MINGW64:
    import distutils.cygwinccompiler
    distutils.cygwinccompiler.get_msvcr = lambda: []

# Update these with new releases
__version__ = "0.0.2"
endless_sky_version = "753db45e921b7b7d57bb7b4afaf5181acbe0a6cc"

# TODO use info at https://pybind11.readthedocs.io/en/stable/compiling.html
# to speed this up

extra_compile_args=[
        '-Wno-deprecated-declarations', # ignore mac OpenGL deprecation warnings
        ] if platform.system() == "Darwin" else []

extra_link_args = (["-Wl"] if platform.system() == "Windows" else [])

pybind_extension = Pybind11Extension("endless_sky.bindings", [
        "endless_sky/lib.cpp",
        "endless_sky/endless-sky/tests/src/helpers/datanode-factory.cpp",
    ] + sorted(
        glob('endless_sky/endless-sky/source/*.cpp') +
        glob('endless_sky/endless-sky/source/text/*.cpp')
    ),
    libraries=[
        "winmm",
        "mingw32",
        "sdl2main",
        "sdl2.dll",
        "png.dll",
        "turbojpeg.dll",
        "jpeg.dll",
        "openal32.dll",
        "rpcrt4",
        "glew32.dll",
        "opengl32",
        'mad',
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
    library_dirs=[
        './dev64/lib', # *.dll.a
        './dev64/bin', # *.dll
    #    './dev64/include' # *.h
    ] if platform.system() == "Windows" else [
        # mac homebrew locations
        '/usr/local/opt/jpeg-turbo/lib', 
        '/usr/local/opt/openal-soft/lib',
        '/usr/local/lib/',
        # need linux locations here?
    ],
    include_dirs=[
        os.path.join(path_to_build_folder(), 'endless-sky/tests/include'),
        os.path.join(path_to_build_folder(), 'endless-sky/endless-sky/source/*.h'),
        os.path.join(path_to_build_folder(), 'endless-sky/endless-sky/source/text/*.h'),
    ] + ([
        './dev64/include',
        'endless-sky/tests/include',
    ] if platform.system() == "Windows" else [
        # mac homebrew locations
        '/usr/local/opt/jpeg-turbo/include', # homebrew doesn't link this
    ] if platform.system() == "Mac" else []),
    extra_compile_args=extra_compile_args,
    extra_link_args=extra_link_args,
    define_macros=[
            ('VERSION_INFO', __version__),
            ('ENDLESS_SKY_VERSION_INFO', endless_sky_version),
    ],
    data_files=([
        (
            '', # install in the package folder
            sorted(glob(".\dev64\bin\*.dll")) + [
                DIR_MINGW64 + "\lib\libgcc_s_seh-1.dll",
                DIR_MINGW64 + "\lib\libstdc++-6.dll",
                DIR_MINGW64 + "\lib\libwinpthread-1.dll",
            ]
        )
    ] if platform.system() == "Windows" and DIR_MINGW64 else [])
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
        ]
    },
    extras_require={"test": "pytest"},
    # Currently, build_ext only provides an optional "highest supported C++
    # level" feature, but in the future it may provide more features.
    cmdclass={"build_ext": build_ext},
    zip_safe=False,
)
