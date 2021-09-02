import endless_sky_bindings as m

def test_version():
    assert m.__version__ == '0.0.2'

def test_example_functions():
    assert m.add(1, 2) == 3
    assert m.subtract(1, 2) == -1
