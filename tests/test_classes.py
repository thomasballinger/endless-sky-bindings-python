import endless_sky_bindings as m

def test_point():
    p = m.Point(1, 2)
    assert p.x == 1.0
    assert p.y == 2.0
