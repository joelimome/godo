# vim: ft=python

def other():
    print "ZEBRA"

@task
@cfg.decfun
def task_a():
    print "THIS IS A"
    other()
