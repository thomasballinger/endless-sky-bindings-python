import os
import pytest
import tempfile

from endless_sky.parser import parse

from helpers import icky_global_state

subaru_data = (
'ship Subaru\n'
'\tattributes\n'
'\t\tcategory "Transport"\n'
'\t\t"outfit space" 100\n'
'\t\tdrag 5\n'
'\toutfits\n'
'\t\t"Scram Drive"\n'
)

@pytest.fixture
def subaru(tmp_path):
    r = tmp_path / "subaru.txt"
    r.write_text(subaru_data)
    return r

@icky_global_state
def test_parse_ships(subaru):
    assert os.path.exists('endless_sky/endless-sky'), 'meant to be run in build environment'

    d = parse('ships', str(subaru), format='dict', resources='endless_sky/endless-sky')
    subaru = d['Subaru']
    print(subaru)
    assert subaru['drag'] == 5.0
    assert subaru['scram drive'] == 0.2

@icky_global_state
def test_parse_ships_with_undefined_outfits(subaru):
    d = parse('ships', str(subaru), format='dict')
    subaru = d['Subaru']
    print(subaru)
    assert subaru['drag'] == 5.0
    assert 'scram drive' not in subaru

