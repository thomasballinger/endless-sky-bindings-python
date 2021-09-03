import platform
from setuptools import setup
from glob import glob
import os
import sys

# Available at setup time due to pyproject.toml
from pybind11.setup_helpers import Pybind11Extension, build_ext

DIR_MINGW64 = os.environ.get('DIR_MINGW64')
# DIR_MINGW64 is defined using the already-installed mingw libraries,
# and not defined when using the 

if platform.system() == "Windows" and DIR_MINGW64:
    import distutils.cygwinccompiler
    distutils.cygwinccompiler.get_msvcr = lambda: []

__version__ = "0.0.2"

endless_sky_version = ""

# TODO use info at https://pybind11.readthedocs.io/en/stable/compiling.html
# to speed this up

# There are a few options to pursue for Windows:
# - try to link everything statically!
# - 

extra_compile_args=[
        '-Wno-deprecated-declarations', # ignore mac OpenGL deprecation warnings
        ] if platform.system() == "Darwin" else [
        ]

extra_link_args = (["-Wl,-Bstatic", "-lpthread", "-static-libstdc++", "-static"]
                   if platform.system() == "Windows" else [])

ext_modules = [
    Pybind11Extension("endless_sky_bindings", [
            "lib.cpp",
            "endless-sky/tests/src/helpers/datanode-factory.cpp",
        ] + sorted(
            glob('endless-sky/source/*.cpp') +
            glob('endless-sky/source/text/*.cpp')
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
            #'./dev64/lib', try to force the dlls in bin
            './dev64/bin', # which of these is correct?
            './dev64/include'
        ] if platform.system() == "Windows" else [
            # mac homebrew locations
            '/usr/local/opt/jpeg-turbo/lib', 
            '/usr/local/opt/openal-soft/lib',
            '/usr/local/lib/',
            # need linux locations here?
        ],
        include_dirs=[
            './dev64/include',
            'endless-sky/tests/include',
        ] if platform.system() == "Windows" else [
            # mac homebrew locations
            'endless-sky/tests/include',
            '/usr/local/opt/jpeg-turbo/include',
        ],
        extra_compile_args=extra_compile_args,
        extra_link_args=extra_link_args,
        define_macros=[('VERSION_INFO', __version__)],
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
    ),
]

setup(
    name="endless-sky-bindings",
    version=__version__,
    author="Thomas Ballinger",
    author_email="thomasballinger@gmail.com",
    url="https://github.com/thomasballinger/endless-sky-bindings-python",
    description="Python bindings for Endless Sky C++ code",
    long_description="",
    ext_modules=ext_modules,
    packages=['endless_sky'],
    extras_require={"test": "pytest"},
    # Currently, build_ext only provides an optional "highest supported C++
    # level" feature, but in the future it may provide more features.
    cmdclass={"build_ext": build_ext},
    zip_safe=False,
)
