from glob import glob
import os
import platform
import re
from setuptools import setup
import sys
import sysconfig
import warnings

from pybind11.setup_helpers import Pybind11Extension
from pybind11.setup_helpers import build_ext
from pybind11.setup_helpers import ParallelCompile
from pybind11.setup_helpers import naive_recompile

__version__ = re.search(
    r'__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
    open('endless_sky/__init__.py', encoding='utf_8_sig').read()
).group(1)

endless_sky_version = "2fd9f8883ccc4bcfcd62e9aa12194f0941572543"
submodule_version = None
try:
    submodule_version = open('.git/modules/endless_sky/endless-sky/HEAD').read().strip()
except FileNotFoundError:
    print('Skipping submodule version == endless_sky_version check because no git repo found')
if submodule_version and submodule_version != endless_sky_version:
    msg = "endless_sky_version "+endless_sky_version+" does not match submodule "+submodule_version
    warnings.warn(msg)
    if (os.environ.get('GITHUB_REPOSITORY') or '').endswith("endless-sky-bindings-python"):
        # todo: prevent doing a release without updating this? currently doesn't run
        raise ValueError(msg)

ParallelCompile(needs_recompile=naive_recompile).install()

# Endless Sky requires libraries like dirent.h that are not provided by MSVC,
# so mingw should be used when compiling on Windows.
# However Pybind11Extension seems to assume MVSC on the windows platform, so
# monkey-patch PyBindExtension to convert \foo flags to -foo because it adds
# some \args style args on Windows assuming we're using compiler that likes them.
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

# There are two different styles of sdists builds possible.
# With ES_SETUP_INCLUDE_LIBRARIES=1 (eg when building wheels) we copy
# in all libraries into endless_sky/lib. This produces a build that only
# works on a single platform because we harvest the libraries from the system.
# Without ES_SETUP_INCLUDE_LIBRARIES set (eg when the package will be run on
# the very same machine that is building it) we do not copy these libraries in
# and just look for library folders on the OS.
INCLUDE_LIBRARIES = (os.environ.get('ES_SETUP_INCLUDE_LIBRARIES') or '0') == '1'
print('INCLUDE_LIBRARIES:', INCLUDE_LIBRARIES)

# Once we have an sdist we use the presence of endless_sky/lib to determine
# whether to use the system lib locations or the local ones.
LIBRARIES_INCLUDED = os.path.exists('endless_sky/lib/')
print('LIBRARIES_INCLUDED:', LIBRARIES_INCLUDED)

if INCLUDE_LIBRARIES:
    assert LIBRARIES_INCLUDED, "can't include libraries if endless_sky/lib/ does not exist. Run ./grab_libraries.py to harvest libs from the OS."

assert os.path.exists('endless_sky/endless-sky/'), "endless-sky sources not present. Did you not git clone --recursive?"

# https://stackoverflow.com/questions/63804883/including-and-distributing-third-party-libraries-with-a-python-c-extension
def path_to_build_folder():
    """Returns the name of a distutils build directory"""
    f = "{dirname}.{platform}-{version[0]}.{version[1]}"
    dir_name = f.format(dirname='lib',
                    platform=sysconfig.get_platform(),
                    version=sys.version_info)
    return os.path.join('build', dir_name, 'endless_sky')

# https://stackoverflow.com/a/57109148/398212
# TODO do we also need extra_link_args = ["-Wl,-Bstatic", "-lpthread"] ? Would that help with our threading issues?
if platform.system() == "Windows":
    import distutils.cygwinccompiler
    # monkeypatch for too-recent MSVC versions
    distutils.cygwinccompiler.get_msvcr = lambda: []

# Python package builds happen in two steps: an sdist is always created first,
# then a wheel is optionally created based on that sdist. (I think.)
# All necessary dylib/so/DLL files need to be included in the sdist OR
# instructions about how to install them need to be included in the README.
# This seems hard on Windows, so the goal here is to not require anything else
# to be installed on that platform.
# So Windows DLLs will be included in the sdist, but mac and linux libs needn't
# be since on those platform telling someone to install libraries isn't so bad.
# We do including libpeg-turbo and openal-soft in the mac build, and maybe we
# could include more libraries here too?
# Whether any libraries are linked depends on the INCLUDE_LIBRARIES env variable.

def crash(msg=''):
    raise AssertionError((msg or 'TODO') + ' on platform ' + platform.system())

# TODO use info at https://pybind11.readthedocs.io/en/stable/compiling.html
# to speed this compile process up when iterating.
extra_compile_args=[
        '-DES_NO_THREADS',  # This will only have an effect if endless-sky is
                            # patched with patch.diff, adding the option to
                            # build this code without threads.
        '-Wno-deprecated-declarations', # ignore mac OpenGL deprecation warnings
            #'-v',  # for debugging an include
            #'-H',  # for debugging an include
        ] if platform.system() == "Darwin" else [
            '-DES_NO_THREADS',
            #'-v',  # for debugging an include
            #'-H',  # for debugging an include
            '-fvisibility=hidden',
            '-g0',
        ] if platform.system() == "Windows" else [
            '-DES_NO_THREADS',  # Windows is the only platform that actually
                                # needs the threadless build, but we do it
                                # everywhere for consistency.
        ]

extra_link_args = ([
    #'-Wl,--verbose'  # for debugging
    ] if platform.system() == "Windows" else [
    "-Wl,-rpath,$ORIGIN/lib/." # On Mac and Linux this adds our lib folder.
                               # On windows this is taken care of at runtime,
                               # see endless_sky/libpath_hack.py.
])

pybind_extension = Pybind11Extension("endless_sky.bindings", [
        "endless_sky/lib.cpp",
        "endless_sky/endless-sky/tests/src/helpers/datanode-factory.cpp",

        # eventually this should just be a glob, but I'm listing
        # files to see which ones cause the hang on exit on Windows.
        #] + glob('endless_sky/endless-sky/source/*.cpp') +
        #glob('endless_sky/endless-sky/source/text/*.cpp'),
        "endless_sky/endless-sky/source/AI.cpp",
        "endless_sky/endless-sky/source/Account.cpp",
        "endless_sky/endless-sky/source/Angle.cpp",
        "endless_sky/endless-sky/source/Armament.cpp",
        "endless_sky/endless-sky/source/AsteroidField.cpp",
        "endless_sky/endless-sky/source/Audio.cpp",
        "endless_sky/endless-sky/source/BankPanel.cpp",
        "endless_sky/endless-sky/source/BatchDrawList.cpp",
        "endless_sky/endless-sky/source/BatchShader.cpp",
        "endless_sky/endless-sky/source/BoardingPanel.cpp",
        "endless_sky/endless-sky/source/Body.cpp",
        "endless_sky/endless-sky/source/CaptureOdds.cpp",
        "endless_sky/endless-sky/source/CargoHold.cpp",
        "endless_sky/endless-sky/source/CollisionSet.cpp",
        "endless_sky/endless-sky/source/Color.cpp",
        "endless_sky/endless-sky/source/Command.cpp",
        "endless_sky/endless-sky/source/ConditionSet.cpp",
        "endless_sky/endless-sky/source/Conversation.cpp",
        "endless_sky/endless-sky/source/ConversationPanel.cpp",
        "endless_sky/endless-sky/source/CoreStartData.cpp",
        "endless_sky/endless-sky/source/DataFile.cpp",
        "endless_sky/endless-sky/source/DataNode.cpp",
        "endless_sky/endless-sky/source/DataWriter.cpp",
        "endless_sky/endless-sky/source/Date.cpp",
        "endless_sky/endless-sky/source/Depreciation.cpp",
        "endless_sky/endless-sky/source/Dialog.cpp",
        "endless_sky/endless-sky/source/Dictionary.cpp",
        "endless_sky/endless-sky/source/DistanceMap.cpp",
        "endless_sky/endless-sky/source/DrawList.cpp",
        "endless_sky/endless-sky/source/Effect.cpp",
        "endless_sky/endless-sky/source/Engine.cpp",
        "endless_sky/endless-sky/source/EsUuid.cpp",
        "endless_sky/endless-sky/source/EscortDisplay.cpp",
        "endless_sky/endless-sky/source/File.cpp",
        "endless_sky/endless-sky/source/Files.cpp",
        "endless_sky/endless-sky/source/FillShader.cpp",
        "endless_sky/endless-sky/source/Fleet.cpp",
        "endless_sky/endless-sky/source/Flotsam.cpp",
        "endless_sky/endless-sky/source/FogShader.cpp",
        "endless_sky/endless-sky/source/FrameTimer.cpp",
        "endless_sky/endless-sky/source/Galaxy.cpp",
        "endless_sky/endless-sky/source/GameData.cpp",
        "endless_sky/endless-sky/source/GameEvent.cpp",
        "endless_sky/endless-sky/source/GameWindow.cpp",
        "endless_sky/endless-sky/source/Government.cpp",
        "endless_sky/endless-sky/source/HailPanel.cpp",
        "endless_sky/endless-sky/source/Hardpoint.cpp",
        "endless_sky/endless-sky/source/Hazard.cpp",
        "endless_sky/endless-sky/source/HiringPanel.cpp",
        "endless_sky/endless-sky/source/ImageBuffer.cpp",
        "endless_sky/endless-sky/source/ImageSet.cpp",
        "endless_sky/endless-sky/source/Information.cpp",
        "endless_sky/endless-sky/source/Interface.cpp",
        "endless_sky/endless-sky/source/ItemInfoDisplay.cpp",
        "endless_sky/endless-sky/source/LineShader.cpp",
        "endless_sky/endless-sky/source/LocationFilter.cpp",
        "endless_sky/endless-sky/source/LogbookPanel.cpp",
        "endless_sky/endless-sky/source/MainPanel.cpp",
        "endless_sky/endless-sky/source/MapDetailPanel.cpp",
        "endless_sky/endless-sky/source/MapOutfitterPanel.cpp",
        "endless_sky/endless-sky/source/MapPanel.cpp",
        "endless_sky/endless-sky/source/MapSalesPanel.cpp",
        "endless_sky/endless-sky/source/MapShipyardPanel.cpp",
        "endless_sky/endless-sky/source/Mask.cpp",
        "endless_sky/endless-sky/source/Messages.cpp",
        "endless_sky/endless-sky/source/Minable.cpp",
        "endless_sky/endless-sky/source/Mission.cpp",
        "endless_sky/endless-sky/source/MissionAction.cpp",
        "endless_sky/endless-sky/source/MissionPanel.cpp",
        "endless_sky/endless-sky/source/Mortgage.cpp",
        "endless_sky/endless-sky/source/Music.cpp",
        "endless_sky/endless-sky/source/NPC.cpp",
        "endless_sky/endless-sky/source/News.cpp",
        "endless_sky/endless-sky/source/Outfit.cpp",
        "endless_sky/endless-sky/source/OutfitInfoDisplay.cpp",
        "endless_sky/endless-sky/source/OutfitterPanel.cpp",
        "endless_sky/endless-sky/source/OutlineShader.cpp",
        "endless_sky/endless-sky/source/Panel.cpp",
        "endless_sky/endless-sky/source/Person.cpp",
        "endless_sky/endless-sky/source/Personality.cpp",
        "endless_sky/endless-sky/source/Phrase.cpp",
        "endless_sky/endless-sky/source/Planet.cpp",
        "endless_sky/endless-sky/source/PlanetLabel.cpp",
        "endless_sky/endless-sky/source/PlanetPanel.cpp",
        "endless_sky/endless-sky/source/PlayerInfo.cpp",
        "endless_sky/endless-sky/source/PlayerInfoPanel.cpp",
        "endless_sky/endless-sky/source/Point.cpp",
        "endless_sky/endless-sky/source/PointerShader.cpp",
        "endless_sky/endless-sky/source/Politics.cpp",
        "endless_sky/endless-sky/source/Preferences.cpp",
        "endless_sky/endless-sky/source/Projectile.cpp",
        "endless_sky/endless-sky/source/Radar.cpp",
        "endless_sky/endless-sky/source/Random.cpp",
        "endless_sky/endless-sky/source/Rectangle.cpp",
        "endless_sky/endless-sky/source/RingShader.cpp",
        "endless_sky/endless-sky/source/SavedGame.cpp",
        "endless_sky/endless-sky/source/Screen.cpp",
        "endless_sky/endless-sky/source/Shader.cpp",
        "endless_sky/endless-sky/source/Ship.cpp",
        "endless_sky/endless-sky/source/ShipEvent.cpp",
        "endless_sky/endless-sky/source/ShipInfoDisplay.cpp",
        "endless_sky/endless-sky/source/ShipInfoPanel.cpp",
        "endless_sky/endless-sky/source/ShipyardPanel.cpp",
        "endless_sky/endless-sky/source/ShopPanel.cpp",
        "endless_sky/endless-sky/source/Sound.cpp",
        "endless_sky/endless-sky/source/SpaceportPanel.cpp",
        "endless_sky/endless-sky/source/Sprite.cpp",
        "endless_sky/endless-sky/source/SpriteQueue.cpp",
        "endless_sky/endless-sky/source/SpriteSet.cpp",
        "endless_sky/endless-sky/source/SpriteShader.cpp",
        "endless_sky/endless-sky/source/StarField.cpp",
        "endless_sky/endless-sky/source/StartConditions.cpp",
        "endless_sky/endless-sky/source/StellarObject.cpp",
        "endless_sky/endless-sky/source/System.cpp",
        "endless_sky/endless-sky/source/Test.cpp",
        "endless_sky/endless-sky/source/TestData.cpp",
        "endless_sky/endless-sky/source/Trade.cpp",
        "endless_sky/endless-sky/source/TradingPanel.cpp",
        "endless_sky/endless-sky/source/UI.cpp",
        "endless_sky/endless-sky/source/Visual.cpp",
        "endless_sky/endless-sky/source/Weapon.cpp",
        "endless_sky/endless-sky/source/Weather.cpp",
        "endless_sky/endless-sky/source/text/DisplayText.cpp",
        "endless_sky/endless-sky/source/text/Font.cpp",
        "endless_sky/endless-sky/source/text/FontSet.cpp",
        "endless_sky/endless-sky/source/text/Format.cpp",
        "endless_sky/endless-sky/source/text/Table.cpp",
        "endless_sky/endless-sky/source/text/Utf8.cpp",
        "endless_sky/endless-sky/source/text/WrappedText.cpp",

        # Not needed by GameData, so not yet included (but TODO just use everything)
        #"endless_sky/endless-sky/source/main.cpp",
        #"endless_sky/endless-sky/source/LoadPanel.cpp",
        #"endless_sky/endless-sky/source/MenuPanel.cpp",
        #"endless_sky/endless-sky/source/PreferencesPanel.cpp",
        #"endless_sky/endless-sky/source/StartConditionsPanel.cpp",
    ],
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
    library_dirs=(
        [os.path.join(path_to_build_folder(), 'lib')] if LIBRARIES_INCLUDED else (
            [
                # TODO can we include everything so no brew install is required?
                '/usr/local/opt/jpeg-turbo/lib',
                '/usr/local/opt/openal-soft/lib',
            ] if platform.system() == 'Darwin' else [
                #TODO does anything need to be manually included here?
                # Probably not, linux libs will just be in the right spots?
            ] if platform.system() == 'Linux' else [
                 './dev64/lib', # *.dll.a - should be included at compile time
                                #           but could be removed from wheel
                 './dev64/bin', # *.dll
            ] if platform.system() == "Windows" else crash())),
    include_dirs=(
        ([os.path.join(path_to_build_folder(), 'include')] if LIBRARIES_INCLUDED else (
            [
                '/usr/local/opt/jpeg-turbo/include',
                '/usr/local/opt/openal-soft/include',
            ] if platform.system() == 'Darwin' else [
                #TODO does anything need to be manually included here?
                # Probably not, linux probably just works?
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
    version=__version__,          # want to prove out the library before asking
                                  # for permission to do that.
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
    cmdclass={"build_ext": build_ext},
    zip_safe=False,
)
