import os

import pytest

from endless_sky.loader import load_string_data, LoadedData
from endless_sky.loader import AlreadyLoadedError

from helpers import icky_global_state, empty_resources_dir, empty_config_dir

sailboat_data = (
'ship Sailboat\n'
'\tattributes\n'
'\t\tdrag 8\n'
'\toutfits\n'
'\t\t"Scram Drive"\n'
)

paddleboard_data = (
'ship Paddleboard\n'
'\tattributes\n'
'\t\tdrag 12\n'
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
    load_string_data(sailboat_data, resources='endless_sky/endless-sky')
    with pytest.raises(AlreadyLoadedError):
        load_string_data(sailboat_data, resources='endless_sky/endless-sky')

@icky_global_state
def test_load_with_existing_config(empty_resources_dir, empty_config_dir, sailboat):
    (empty_config_dir / "plugins" / "myplugin").mkdir()
    (empty_config_dir / "plugins" / "myplugin" / "data").mkdir()
    (empty_config_dir / "plugins" / "myplugin" / "data" / "lakeships.txt").write_text(paddleboard_data)
    with LoadedData(
            path=str(sailboat),
            resources=str(empty_resources_dir),
            config=str(empty_config_dir)) as es:
        assert es.GameData.Ships().Find("Sailboat")
        assert es.GameData.Ships().Find("Paddleboard")

    # make sure existing plugins don't accidentally get deleted
    assert (empty_config_dir / "plugins" / "myplugin" / "data" / "lakeships.txt").read_text() == paddleboard_data

