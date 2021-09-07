import json
from contextlib import contextmanager
from pathlib import Path

from .loader import LoadedData

from pprint import pformat

#formats are json, dict, and pretty

def parse_ships(path, format='dict', *, resources_path=None, config_path=None):
    with LoadedData(path, resources_path=resources_path, config_path=config_path) as es:
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
