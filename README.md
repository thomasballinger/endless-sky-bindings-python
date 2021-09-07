Endless Sky bindings for Python

$ pip install endless-sky-bindings

This library does not include the Endless Sky data, so you'll need to find that on your system or clone the [Endless Sky repo](https://github.com/endless-sky/endless-sky) to get it.

## Command line use

```
% echo -e 'ship Rocket\n\tattributes\n\t\tdrag 10' > myData.txt
$ python -m endless_sky parse --resources ~/endless-sky myData.txt# only parses ships atm
...
 'Rocket': {'drag': 10.0, 'gun ports': 0.0, 'turret mounts': 0.0},
...
```

## Library

Once you get a handle on the endless_sky.bindings module (bound to 'es' variable here),
C++ classes are exposed to Python pretty directly; for documentation, see
[the header files in Endless Sky](https://github.com/endless-sky/endless-sky/tree/master/source).

```
>>> from endless_sky.parser import load_data
>>> es = load_data(resources="/Users/tomb/endless-sky")
>>> es.Ship
<class 'endless_sky.bindings.Ship'>
>>> ships = es.GameData.Ships() # these objects correspond to 
>>> ships.<tab><tab>
ships.Find(  ships.Has(   ships.size(
>>> ships.Find("Shuttle")
<endless_sky.bindings.Ship object at 0x1087391b0>
>>> shuttle = ships.Find("Shuttle")
>>> shuttle.<tab><tab>
shuttle.Attributes(      shuttle.Cost(            shuttle.FlightCheck(     shuttle.Place(
shuttle.BaseAttributes(  shuttle.Description(     shuttle.ModelName(       shuttle.Recharge(
shuttle.ChassisCost(     shuttle.FinishLoading(   shuttle.Name(            shuttle.SetName(
>>> shuttle.Attributes().Attributes()
<endless_sky.bindings.Dictionary object at 0x1087392f0>
>>> dict(shuttle.Attributes().Attributes())
{'bunks': 6.0, 'cargo space': 20.0, 'drag': 1.7000000000000002, ...}
>>> shuttle.SetName("Summer Breeze"...)
>>> x = ships.Find("Shuttle")
>>> x.Name()
'Summer Breeze'
```

Warning: endless_sky.bindings contains non-resetable singletons like GameData, so once you load some data (directly with GameData.BeginLoad(), with a load_data, or indirectly with a parser function) you can't unload that data without exiting Python.

## Run the game
```
>>> from endless_sky import bindings
>>> bindings.main(['asdf', '--resources', '/Users/tomb/endless-sky'])

```

# Notes

- You can only load once!
- Loading takes a lot of memory: 600MB for vanilla data! (this could be optimized)

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

# Dev notes

## Updating the Endless Sky patch

These bindings use a patched version of Endless Sky to patch out threads and make a few other changes.

To update the patch:

- make changes in the submodule at endless_sky/endless-sky
- with that directory as the working directory, run `git diff > ../../patch.diff`

This is likely to be necessary after updating the version of Endless Sky used.

This patch is intended to be the minimum to make Python bindings work; if this repo is combined with Emscripten-compiled JavaScript bindings at a later date it will need to be expanded.
