import os
from pprint import pprint

from endless_sky.loader import LoadedStringData

def test_ships():
    assert os.path.exists('endless_sky/endless-sky'), 'meant to be run in build environment'
    s = (
    'ship Canoe\n'
    '\tattributes\n'
    '\t\tcategory "Transport"\n'
    '\t\tdrag 50\n'
    '\thas outfits:\n'
    '\t\t1 Scram Drive\n'
    )

    with LoadedStringData(s, resources_path='endless_sky/endless-sky') as es:
        ships = es.GameData.Ships()
        canoe = ships.Find("Canoe")
        canoe.FinishLoading(True)
        print(canoe.Attributes().Attributes())
        #assert 0
