# vim: ft=python

@task
def foo():
    ret = run('ls')
    print "godo.cfg.py at %d" % ret.find("godo.cfg.py")

