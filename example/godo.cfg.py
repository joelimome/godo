
import os

myvalue = "Hello godo world!"

def cfgfun():
    assert os.path.split(__file__)[1] == "godo.cfg.py", "Name: %s" % __file__
    return os.path.isfile(__file__)
