# vim: ft=python

import os

@task
def uname():
    print "Uname: %s" % os.uname()[0]

