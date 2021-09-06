Endless Sky bindings for Python

$ pip install endless-sky-bindings

This library does not include the Endless Sky data, so you'll need to find that on your system or clone the [Endless Sky repo](https://github.com/endless-sky/endless-sky) to get it.

```
>>> import endless_sky.bindings as es
>>> from pprint import pprint
>>> es.GameData.BeginLoad(['foo', '--resources', '/Users/tomb/endless-sky/'])
True
>>> ships = es.GameData.Ships()
>>> shuttle = ships.Find("Shuttle")
>>> shuttle.FinishLoading(True)
>>> pprint(dict(shuttle.Attributes().Attributes()))
{'bunks': 6.0,
 'cargo space': 20.0,
 'drag': 1.7000000000000002,
 'energy capacity': 1000.0,
 'energy generation': 1.2000000000000002,
 'engine capacity': 13.0,
 'fuel capacity': 400.0,
 'gun ports': 1.0,
 ...
```

# Installation

## Mac

```
brew install libmad libpng SDL2
pip install endless-sky-bindings
```

## Linux

```
sudo apt-get install libsdl2-dev libpng-dev libjpeg-turbo8-dev libopenal-dev libmad0-dev libglew-dev libgl1-mesa-dev libegl1-mesa-dev libgles2-mesa-dev uuid-dev
pip install endless-sky-bindings
```

## Windows

```
pip install endless-sky-bindings
```

# Building from source

```
git clone git@github.com:thomasballinger/endless-sky-bindings-python.git
cd endless-sky-bindings-python
```

---

Mac
```
brew install libmad libpng jpeg-turbo SDL2 openal-soft
```

Linux
```
sudo apt-get install libsdl2-dev libpng-dev libjpeg-turbo8-dev libopenal-dev libmad0-dev libglew-dev libgl1-mesa-dev libegl1-mesa-dev libgles2-mesa-dev uuid-dev
```

Windows
```
Invoke-WebRequest https://endless-sky.github.io/win64-dev.zip -OutFile win64-dev.zip
Expand-Archive win64-dev.zip -DestinationPath . -Force
Remove-Item win64-dev.zip
```

---

```
cd endless_sky/endless-sky
patch -p1 < ../../patch.diff
cd ../..
pip install 
```

# Updating the Endless Sky patch

These bindings use a patched version of Endless Sky to patch out threads and make a few other changes.

To update the patch:

- make changes in the submodule at endless_sky/endless-sky
- with that directory as the working directory, run `git diff > ../../patch.diff`

This is especially important after updating the version of Endless Sky used.

This patch is intended to be the minimum to make Python bindings work; if this repo is combined with Emscripten-compiled JavaScript bindings at a later date it will need to be expanded.
