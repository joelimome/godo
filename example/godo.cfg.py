
import functools
import os

myvalue = "Hello godo world!"

def myfun():
    assert os.path.split(__file__)[1] == "godo.cfg.py", "Name: %s" % __file__
    return os.path.isfile(__file__)

def decfun(fun):
    @functools.wraps(fun)
    def noticerun():
        print "Running function: %s" % fun.func_name
        try:
            fun()
        except:
            raise
    return noticerun
