import endless_sky_bindings as m
import platform

def test_random():
    m.RandomSeed(123);
    if platform.system() == 'Darwin':
        assert m.RandomInt(10) == 5;
    elif platform.system() == 'Linux':
        assert m.RandomInt(10) == 3;
