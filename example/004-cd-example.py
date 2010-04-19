
import os

@task
def withcd():
    cwd = os.path.dirname(__file__)
    upone = os.path.dirname(cwd)
    with cd(upone):
        cwd = os.path.abspath(os.getcwd())
        upone = os.path.abspath(upone)
        assert cwd == upone, "Wrong directory: %s" % cwd
        print "Yay! %s" % upone
