import json
from pathlib import Path

from .loader import load_data

from pprint import pformat

#formats are json, dict, and pretty

def parse_ships(path=None, *, resources=None, config=None, format='dict'):
    """
    Parse a file or folder along with resources

    """
    es = load_data(path, resources=resources, config=config)
    ships = es.GameData.Ships()
    for name, ship in ships:
        ship.FinishLoading(True)
    all_ship_data = {name: dict(ship.Attributes().Attributes()) for name, ship in list(ships)}
    if format == 'json':
        return json.dumps(all_ship_data)
    elif format == 'dict':
        return all_ship_data
    elif format == 'pretty':
        return pformat(all_ship_data)
    else:
        raise ValueError("Bad format specifier")
