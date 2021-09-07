import os

from helpers import icky_global_state

from endless_sky.loader import LoadedStringData

@icky_global_state
def test_ships():
    assert os.path.exists('endless_sky/endless-sky'), 'meant to be run in build environment'
    s = (
    'ship Canoe\n'
    '\tattributes\n'
    '\t\tcategory "Transport"\n'
    '\t\t"outfit space" 100\n'
    '\t\tdrag 10\n'
    '\toutfits\n'
    '\t\t"Scram Drive"\n'
    )

    with LoadedStringData(s, resources_path='endless_sky/endless-sky') as es:
        ships = es.GameData.Ships()
        canoe = ships.Find("Canoe")
        canoe.FinishLoading(True)
        print(list(canoe.Attributes().Attributes()))
        assert canoe.Attributes().Attributes()['scram drive'] == 0.2
