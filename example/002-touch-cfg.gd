# vim: ft=python

@task
def cfgval(cfg):
    print cfg['myvalue']

@task
def cfgfun(cfg):
    print cfg["cfgfun"]()
