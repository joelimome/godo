# vim: ft=python

import os

@task
def cfgval():
    print cfg.myvalue

@task
def cfgfun():
    print cfg.myfun()

@task
def setdel():
    cfg.baz = 2
    assert cfg.baz == 2, "baz not set"
    del cfg.baz
    try:
        cfg.bar
    except AttributeError:
        print "YAY! not found"

@task
@cfg.decfun
def stuff_here():
    print "We have been decorated."

def otherfun():
    print "OHAI!"

@task
@cfg.decfun
def with_global():
    print globals().keys()
    print os
    otherfun()
