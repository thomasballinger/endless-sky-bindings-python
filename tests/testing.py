import endless_sky.bindings as m
import os

def test_Point():
    p = m.Point(1, 2)
    assert p.X == 1
    assert p.Y == 2

test_Point()

print("ran code")

print("now let's try to exit")

os._exit(0)



