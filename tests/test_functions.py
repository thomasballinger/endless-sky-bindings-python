import endless_sky_bindings as m

def test_random():
    m.RandomSeed(123);
    assert m.RandomInt(10) == 5;
