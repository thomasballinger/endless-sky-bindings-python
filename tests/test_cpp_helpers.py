import pytest

from endless_sky import bindings as es

def test_saves_directory():
    # TODO how to test this? it creates a directory!
    assert 'ndless' in es.saves_directory()

def test_plugins_directory():
    # TODO how to test this? it creates a directory!
    assert 'plugins' in es.plugins_directory()

