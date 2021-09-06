import endless_sky.bindings as m
import platform

def test_random():
    m.RandomSeed(123);
    if platform.system() == 'Darwin':
        assert m.RandomInt(10) == 5;
    elif platform.system() == 'Linux':
        assert m.RandomInt(10) == 3;
    # TODO add Windows (but also maybe get rid of this test, it probably
    # depends on system libraries and isn't stable)
