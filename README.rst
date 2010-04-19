GoDo
====

Execute a directory of python code following the definition order.

Given a directory structure that looks like such::

    myscripts/
        1-init.gd
        2-run/
            1-stuff-a.gd
            2-stuff-b.gd
        3-finish.gd

GoDo will traverse through this directory running tasks defined in each file.

Tasks are defined as a function decorated with a ``@task`` decorator. Tasks
defined in a file will be executed in the order in which they are defined.

Task Files
----------

Any file ending in .gd will be read and evaluated as a Python source file. Any
function that is decorated by a the ``@task`` decorator will be added to the
list of tasks to execute.

Example ``mytasks.gd``::

    import os

    @task
    def first_task():
        print "Yay going and doing stuff!"

    @task
    def second_task(cfg):
        print "A config option: %s" % cfg["whee"]


Tasks are executed from the same directory where the file that defines them
is located.

Complete task file API:

  * ``@task`` - Decorate a function so that it will be executed.
  * ``cd(path)`` - Used in ``with`` statements to change the working directory.
  * ``run(cmd)`` - Run a shell command checking the return code.
  * ``sudo(cmd)`` - Prepends a command with sudo. Probably won't work if you
    don't use passwordless sudo. Obviously, that should be fixed.

Config Files
------------

By default, GoDo will look in the base execution directory for a ``godo.cfg.py``
file. (The base execution directory is ``./`` unless specified on the command
line). Alternatively you can specify a path. If a config file is found it is
evaluated and passed as a dictionary to any task function that takes an
argument.


