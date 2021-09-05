Endless Sky bindings for Python


---

Currently stuck trying to get Windows to run!

I'm trying to figure out why my Python ES bindings are passing tests but then hanging on Python interpreter exit on Windows: `sys._exit(0)` hangs if the extension module has been imported, but it can kill itself with `subprocess.call(['Taskkill', '/PID', str(os.getpid(), '/F'])` before this.

I don't know much about Windows. Maybe I want to get remote windows box that looks like the GitHub Actions environment and try to figure out what is going on.

Maybe I should use something similar to strace to instrument just what Python is doing, `python -vv` does give me much.

Maybe I want to start commenting out code in Endless Sky source files; it starts failing once I include GameData and all the files it needs to be linked against, but unfortunately that was a jump from ~60 .cpp files to ~120 .cpp files so there's a lot of code to "bisect."

Probably I should read more about what pybind11 makes things do on exit. I don't understand well what C++ code is running on import / extension module initialization.

Maybe I should try patching threads out again, I've been using the raw Endless Sky source but I have the threadless patch I use for the JavaScript bindings around.

Maybe I should publish the module with this bug and someone on Windows could help me out with debugging. I could write a test running script that runs pytest then forcibly kills the process.


----

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

There will be wheels! They should be easy to install!


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

# Building from source distribution:

## Mac
Install some dependencies

```
brew install libmad libpng jpeg-turbo SDL2 openal-soft
pip install --no-binary endless_sky
```


## Linux

```
sudo apt-get install libsdl2-dev libpng-dev libjpeg-turbo8-dev libopenal-dev libmad0-dev libglew-dev libgl1-mesa-dev libegl1-mesa-dev libgles2-mesa-dev uuid-dev
pip install --no-binary endless_sky
```


## Windows

Download the Windows dependencies from https://endless-sky.github.io/win64-dev.zip and unzip this into a folder called dev64 at the root of the repo. Run python setup.py install.

I don't know if this works, I haven't tried it.
