# vim: ft=python

@task
def cfgval(cfg):
    print cfg.myvalue

@task
def cfgfun(cfg):
    print cfg.myfun()

@task
def setdel(cfg):
    cfg.baz = 2
    assert cfg.baz == 2, "baz not set"
    del cfg.baz
    try:
        cfg.bar
    except AttributeError:
        print "YAY! not found"
