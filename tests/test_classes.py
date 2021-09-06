import pytest
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

def test_GameData_empty(empty_resources_dir, empty_config_dir):
    m.GameData.BeginLoad([
        "progname",
        "--resources", str(empty_resources_dir),
        "--config", str(empty_config_dir),
    ])

def test_GameData_simple(empty_resources_dir, empty_config_dir):
    (empty_resources_dir / "data" / "simple.txt").write_text('ship Canoe\n\tdescription "A boat."')
    m.GameData.BeginLoad([
        "progname",
        "--resources", str(empty_resources_dir),
        "--config", str(empty_config_dir),
    ])
    ships = m.GameData.Ships();
    assert list(ships) == [("Canoe", ships.Find("Canoe"))]

def test_GameData_ownership(empty_resources_dir, empty_config_dir):
    (empty_resources_dir / "data" / "simple.txt").write_text('ship Canoe\n\tdescription "A boat."')
    m.GameData.BeginLoad([
        "progname",
        "--resources", str(empty_resources_dir),
        "--config", str(empty_config_dir),
    ])
    ships = m.GameData.Ships();
    canoe = ships.Find("Canoe")
    del canoe  # segfault if Find used the default return value policy

# This library does not ship with vanilla data, but it's always present in the
# build enviroment so we might as well use it.
def test_GameData_full(empty_config_dir):
    m.GameData.BeginLoad([
        "progname",
        "--resources", "./endless_sky/endless-sky",
        "--config", str(empty_config_dir),
    ])
    assert len(m.GameData.Ships()) > 100
