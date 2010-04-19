# vim: ft=python

import os

@task
def withcd():
    root = "/"
    cwd = os.getcwd()
    assert root != cwd
    with cd(root):
        assert os.getcwd() == root
    assert os.getcwd() == cwd
    print "Yay changed to and back"
