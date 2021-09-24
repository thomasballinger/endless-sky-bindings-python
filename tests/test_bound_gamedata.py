"""
Loading is tricky to test: a new Python process is needed each time because of
global state in GameData.

The hacky approach here is to run pytest in a subproces on just that one test.
"""

import pytest
import subprocess
import sys
import platform
import os
import gc

import endless_sky.bindings as m
from helpers import icky_global_state, empty_resources_dir, empty_config_dir


@icky_global_state
def test_GameData_simple(empty_resources_dir, empty_config_dir):
    (empty_resources_dir / "data" / "simple.txt").write_text('ship Canoe\n\tdescription "A boat."')
    m.GameData.BeginLoad([
        "progname",
        "--resources", str(empty_resources_dir),
        "--config", str(empty_config_dir),
    ])
    ships = m.GameData.Ships();
    assert list(ships) == [("Canoe", ships.Find("Canoe"))]

@icky_global_state
def test_GameData_simple1(empty_resources_dir, empty_config_dir):
    (empty_resources_dir / "data" / "simple.txt").write_text('ship Canoe\n\tdescription "A boat."')
    m.GameData.BeginLoad([
        "progname",
        "--resources", str(empty_resources_dir),
        "--config", str(empty_config_dir),
    ])
    ships = m.GameData.Ships();
    assert list(ships) == [("Canoe", ships.Find("Canoe"))]

@icky_global_state
def test_GameData_simple2(empty_resources_dir, empty_config_dir):
    (empty_resources_dir / "data" / "simple.txt").write_text('ship Kayak\n\tdescription "A sleeker boat for only one."')
    m.GameData.BeginLoad([
        "progname",
        "--resources", str(empty_resources_dir),
        "--config", str(empty_config_dir),
    ])
    ships = m.GameData.Ships();
    assert list(ships) == [("Kayak", ships.Find("Kayak"))]

@icky_global_state
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
@icky_global_state
def test_GameData_full(empty_config_dir):
    m.GameData.BeginLoad([
        "progname",
        "--resources", "./endless_sky/endless-sky",
        "--config", str(empty_config_dir),
    ])
    # This might use a lot of memory (if sprites get loaded)
    assert len(m.GameData.Ships()) > 100

    ships = m.GameData.Ships();
    ships = dict(ships)
    s = ships['Shuttle']
    del ships
    gc.collect()
    del s
    gc.collect()

    govts = m.GameData.Governments();
    govts = dict(govts)
    g = govts['Republic']
    del govts
    gc.collect()
    del g
    gc.collect()

    outfits = m.GameData.Outfits();
    outfits = dict(outfits)
    o = outfits['Hyperdrive']
    del outfits
    gc.collect()
    del o
    gc.collect()

    planets = m.GameData.Planets();
    planets = dict(planets)
    p = planets['Earth']
    del planets
    gc.collect()
    del p
    gc.collect()

    systems = m.GameData.Systems();
    systems = dict(systems)
    s = systems['Sol']
    del systems
    gc.collect()
    del s
    gc.collect()


# This used to segfault
@icky_global_state
def test_GameData_full(empty_config_dir):
    m.GameData.BeginLoad([
        "progname",
        "--resources", "./endless_sky/endless-sky",
        "--config", str(empty_config_dir),
    ])
    earth = m.GameData.Planets().Find("Earth")
    sol = m.GameData.Systems().Find("Sol")
    earth.IsInSystem(sol)
    gc.collect()
