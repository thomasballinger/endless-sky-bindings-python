from setuptools import setup
from glob import glob

# Available at setup time due to pyproject.toml
from pybind11.setup_helpers import Pybind11Extension, build_ext

import sys

__version__ = "0.0.1"

# TODO use info at https://pybind11.readthedocs.io/en/stable/compiling.html
# to speed this up
ext_modules = [
    Pybind11Extension("endless_sky_bindings", [
            "lib.cpp",
            "endless-sky/source/Angle.cpp",
            "endless-sky/source/DataFile.cpp",
            "endless-sky/source/DataNode.cpp",
            "endless-sky/source/File.cpp",
            "endless-sky/source/Files.cpp",
            "endless-sky/source/Point.cpp",
            "endless-sky/source/Random.cpp",
            "endless-sky/source/text/Utf8.cpp",
            "endless-sky/tests/src/helpers/datanode-factory.cpp",
        ],
        libraries=['jpeg', 'SDL2'],
        library_dirs=['/usr/local/opt/jpeg-turbo/lib'],
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
+ sorted(
            glob('endless-sky/source/*.cpp') +
            glob('endless-sky/source/Text/*.cpp')
        ),
"""


setup(
    name="endless_sky_bindings",
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
