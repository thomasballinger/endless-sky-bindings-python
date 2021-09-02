import json

import endless_sky_bindings as es

from pprint import pprint
es.GameData.BeginLoad(['foo', '--resources', '/Users/tomb/endless-sky/'])

ships = es.GameData.Ships()
for name, ship in ships:
    ship.finishLoading()

all_ship_data = {name: dict(ship.Attributes().Attributes()) for name, ship in dict(ships)}
pprint(all_ship_data)
