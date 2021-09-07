import sys
from pprint import pprint

def make_es():
    pprint(sys.modules.keys())
    module_name = 'endless_sky.bindings'
    orig = sys.modules.pop(module_name, None)
    es = __import__(module_name, fromlist=['foo'])
    if orig:
        sys.modules[module_name] = orig
    return es
