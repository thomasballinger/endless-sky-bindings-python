import json
from pathlib import Path

from .loader import load_data

from pprint import pformat

#formats are json, dict, and pretty

def parse(type, path=None, *, resources=None, config=None, format='dict'):
    es = load_data(path, resources=resources, config=config)
    if type == 'ships':
        data = get_ships(es)

    if format == 'json':
        return json.dumps(data)
    elif format == 'dict':
        return data
    elif format == 'pretty':
        return pformat(data)
    else:
        raise ValueError("Bad format specifier")

def get_ships(es):
    ships = es.GameData.Ships()
    for name, ship in ships:
        ship.FinishLoading(True)
    all_ship_data = {name: dict(ship.Attributes().Attributes()) for name, ship in list(ships)}
    return all_ship_data
