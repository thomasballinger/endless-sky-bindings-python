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
    assert d.Tokens() == ["ship", "hello"]

def test_Dictionary():
    d = m.Dictionary()
    assert d

def test_Ship():
    n = m.AsDataNode('ship Canoe\n\tattributes\n\t\tcategory "Transport"')
    s = m.Ship(n)
    assert s.ModelName() == 'Canoe'
