Endless Sky bindings for Python

$ pip install endless-sky-bindings

This library does not include the Endless Sky data, so you'll need to find that on your system or clone the [Endless Sky repo](https://github.com/endless-sky/endless-sky) to get it.

```
>>> import endless_sky_bindings as es
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
 'heat dissipation': 0.8,
 'heat generation': 1.9000000000000001,
 'hull': 600.0,
 'hyperdrive': 1.0,
 'jump fuel': 100.0,
 'jump speed': 0.2,
 'outfit space': 8.0,
 'required crew': 1.0,
 'shield energy': 0.2,
 'shield generation': 0.2,
 'shields': 500.0,
 'thrust': 11.5,
 'thrusting energy': 1.1,
 'thrusting heat': 1.7000000000000002,
 'turn': 307.0,
 'turning energy': 0.6000000000000001,
 'turning heat': 1.1,
 'turret mounts': 0.0,
 'weapon capacity': 10.0}
```
