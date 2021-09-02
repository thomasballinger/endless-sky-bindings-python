import platform
from setuptools import setup
from glob import glob

# Available at setup time due to pyproject.toml
from pybind11.setup_helpers import Pybind11Extension, build_ext

import sys

__version__ = "0.0.2"

# TODO use info at https://pybind11.readthedocs.io/en/stable/compiling.html
# to speed this up

extra_compile_args=[
        '-Wno-deprecated-declarations', # ignore mac OpenGL deprecation warnings
        ]

ext_modules = [
    Pybind11Extension("endless_sky_bindings", [
            "lib.cpp",
            "endless-sky/tests/src/helpers/datanode-factory.cpp",
        ] + sorted(
            glob('endless-sky/source/*.cpp') +
            glob('endless-sky/source/Text/*.cpp')
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
        ] if platform.system() == "Windows" else [
            'jpeg',
            'SDL2',
            'png',
            'openal',
            'mad',
            "uuid"
            "GL",
            "GLEW",
        ],

        library_dirs=[
            # mac homebrew locations
            '/usr/local/opt/jpeg-turbo/lib', 
            '/usr/local/opt/openal-soft/lib',
            '/usr/local/lib/',
            # need linux locations here?
            # windows
            './dev64/lib',
            './dev64/bin', # which of these is correct?
            './dev64/include'
        ],
        include_dirs=[
            # mac homebrew locations
            'endless-sky/tests/include',
            '/usr/local/opt/jpeg-turbo/include',
            # windows
            './dev64/lib',
        ],
        extras_compile_args=extra_compile_args,
        define_macros=[('VERSION_INFO', __version__)],
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
    extras_require={"test": "pytest"},
    # Currently, build_ext only provides an optional "highest supported C++
    # level" feature, but in the future it may provide more features.
    cmdclass={"build_ext": build_ext},
    zip_safe=False,
)
