import pytest
from endless_sky.module_instance_hack import make_es
import endless_sky.bindings as m

def test_Point():
    p = m.Point(1, 2)
    assert p.X == 1
    assert p.Y == 2

def test_Angle():
    a = m.Angle(90)
    assert (a + m.Angle(45)).Degrees()
    a += m.Angle(90)
    assert a.Degrees() == -180

def test_DataNode():
    d = m.AsDataNode('ship hello\n\tkey "value"')
    assert d.HasChildren() is True
    assert d.Size() == 2
    assert d.Token(0) == "ship"
    assert d.Token(1) == "hello"
    assert [x.Token(0) for x in list(d)] == ["key"]

def test_Dictionary():
    d = m.Dictionary()
    assert d

def test_Ship():
    n = m.AsDataNode('ship Canoe\n\tattributes\n\t\tcategory "Transport"')
    s = m.Ship(n)
    assert s.ModelName() == 'Canoe'

@pytest.fixture
def empty_resources_dir(tmp_path):
    r = tmp_path / "resources"
    r.mkdir()
    data = r / "data"; data.mkdir()
    images = r / "images"; images.mkdir()
    sounds = r / "sounds"; sounds.mkdir()
    p = r / "credits.txt"
    p.write_text("some awesome folks\n")
    return r

@pytest.fixture
def empty_config_dir(tmp_path):
    r = tmp_path / "config"
    r.mkdir()
    saves = r / "saves"
    saves.mkdir()
    return r

def test_GameData_simple(empty_resources_dir, empty_config_dir):
    (empty_resources_dir / "data" / "simple.txt").write_text('ship Canoe\n\tdescription "A boat."')
    es = make_es()
    es.GameData.BeginLoad([
        "progname",
        "--resources", str(empty_resources_dir),
        "--config", str(empty_config_dir),
    ])
    ships = es.GameData.Ships();
    assert list(ships) == [("Canoe", ships.Find("Canoe"))]

def test_GameData_simple(empty_resources_dir, empty_config_dir):
    """Check that the hack of importing two modules actually keep data separate."""

    (empty_resources_dir / "data" / "simple.txt").write_text('ship Canoe\n\tdescription "A boat."')
    es1 = make_es()

    es1.GameData.BeginLoad([
        "progname",
        "--resources", str(empty_resources_dir),
        "--config", str(empty_config_dir),
    ])
    ships = es1.GameData.Ships();
    assert list(ships) == [("Canoe", ships.Find("Canoe"))]
    id1 = id(es1)
    del es1

    es2 = make_es()
    assert id1 != id(es2)
    #assert es1 is not es2

    (empty_resources_dir / "data" / "simple.txt").write_text('ship Kayak\n\tdescription "A sleeker boat for only one."')
    print(repr(open(str(empty_resources_dir / "data" / "simple.txt")).read()))
    es2.GameData.BeginLoad([
        "progname",
        "--resources", str(empty_resources_dir),
        "--config", str(empty_config_dir),
    ])
    ships = es2.GameData.Ships();
    assert list(ships) == [("Kayak", ships.Find("Kayak"))]

def test_GameData_ownership(empty_resources_dir, empty_config_dir):
    (empty_resources_dir / "data" / "simple.txt").write_text('ship Canoe\n\tdescription "A boat."')
    es = make_es()
    es.GameData.BeginLoad([
        "progname",
        "--resources", str(empty_resources_dir),
        "--config", str(empty_config_dir),
    ])
    ships = es.GameData.Ships();
    canoe = ships.Find("Canoe")
    del canoe  # segfault if Find used the default return value policy

# This library does not ship with vanilla data, but it's always present in the
# build enviroment so we might as well use it.
def test_GameData_full(empty_config_dir):
    es = make_es()
    es.GameData.BeginLoad([
        "progname",
        "--resources", "./endless_sky/endless-sky",
        "--config", str(empty_config_dir),
    ])
    # This might use a lot of memory (if sprites get loaded)
    assert len(es.GameData.Ships()) > 100
