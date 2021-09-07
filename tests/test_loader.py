import os

import pytest

from endless_sky.loader import load_string_data
from endless_sky.loader import AlreadyLoadedError

from helpers import icky_global_state

sailboat_data = (
'ship Sailboat\n'
'\tattributes\n'
'\t\tdrag 8\n'
'\toutfits\n'
'\t\t"Scram Drive"\n'
)

@pytest.fixture
def sailboat(tmp_path):
    r = tmp_path / "sailboat.txt"
    r.write_text(sailboat_data)
    return r

@icky_global_state
def test_ships():
    assert os.path.exists('endless_sky/endless-sky'), 'meant to be run in build environment'

    es = load_string_data(sailboat_data, resources='endless_sky/endless-sky')
    ships = es.GameData.Ships()
    sailboat = ships.Find("Sailboat")
    sailboat.FinishLoading(True)
    print(list(sailboat.Attributes().Attributes()))
    assert sailboat.Attributes().Attributes()['scram drive'] == 0.2

@icky_global_state
def test_loading_twice():
    with pytest.raises(AlreadyLoadedError):
        load_string_data(sailboat_data, resources='endless_sky/endless-sky')
        load_string_data(sailboat_data, resources='endless_sky/endless-sky')
