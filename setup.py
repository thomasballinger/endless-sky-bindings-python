from setuptools import setup
from glob import glob

# Available at setup time due to pyproject.toml
from pybind11.setup_helpers import Pybind11Extension, build_ext

import sys

__version__ = "0.0.2"

# TODO use info at https://pybind11.readthedocs.io/en/stable/compiling.html
# to speed this up
ext_modules = [
    Pybind11Extension("endless_sky_bindings", [
            "lib.cpp",
            "endless-sky/tests/src/helpers/datanode-factory.cpp",
        ] + sorted(
            glob('endless-sky/source/*.cpp') +
            glob('endless-sky/source/Text/*.cpp')
        ),
        libraries=[
            'jpeg',
            'SDL2',
            'png',
            'openal',
            'mad',
            ],
        library_dirs=[
            '/usr/local/opt/jpeg-turbo/lib',
            '/usr/local/opt/openal-soft/lib',
            '/usr/local/lib/'
            ],
        include_dirs=[
            'endless-sky/tests/include',
            '/usr/local/opt/jpeg-turbo/include'
        ],
        define_macros=[('VERSION_INFO', __version__)],
    ),
]


# TODO use all source files
# - use jpegturbo
# - ignore OPENGL_DEPRECATED on mac
# - 
"""
"""


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
