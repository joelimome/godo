
import contextlib as ctx
import inspect
import logging
import os
import re
import StringIO
import sys

import api
import odict

log = logging.getLogger()

class OutputBuffer(object):
    def __init__(self):
        self.buf = StringIO.StringIO()
    
    def __enter__(self):
        sys.stdout = self.buf
        sys.stderr = self.buf
    
    def __exit__(self, exc_type, exc_inst, traceback):
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

    def getvalue(self):
        return self.buf.getvalue()

class Task(object):
    def __init__(self, path, name, func):
        self.path = path
        self.name = name
        self.func = func
        self.buf = OutputBuffer()
    
    def execute(self):
        with self.buf:
            with api.cd(self.path):
                self.func()

class TaskFile(object):
    DEFAULT_GLOBALS = {
        "__builtins__": __builtins__,
        "__file__": None,
        "__name__": None,
        "__package__": None,
        "task": api.task,
        "cd": api.cd,
        "run": api.run,
        "sudo": api.sudo,
        "cfg": None,
        "log": log
    }
    
    def __init__(self, fname, cfg, depth):
        self.fname = fname
        self.cfg = cfg
        self.depth = depth

        self.glbls = self.DEFAULT_GLOBALS.copy()
        self.glbls.update({
            "__file__": fname,
            "cfg": self.cfg,
        })

        self.tasks = []
        defs = odict.odict()
        execfile(self.fname, self.glbls, defs)
        self.glbls.update(defs)
        for name, func in defs.iteritems():
            if not callable(func) or not getattr(func, "__task__", False):
                continue
            if len(inspect.getargspec(func)[0]) > 0:
                raise ValueError("Invalid task function arity: %s" % name)
            self.tasks.append(Task(os.path.dirname(self.fname), name, func))

    def execute(self):
        for task in self.tasks:
            try:
                log.info("%s-> %s" % (" " * self.depth, task.name))
                task.execute()
            except Exception, inst:
                log.error("Output:\n%s\n%s", "-" * 12, task.buf.getvalue())
                log.exception("Error in task: %s" % task.name)
                sys.exit(1)

class TaskManager(object):
    FNAME_PATTERN = re.compile(r"(^\d+-)?(.*?)(.gd)?$") 

    def __init__(self, cfg, basedir, max_depth=1024):
        self.cfg = cfg
        self.basedir = basedir
        self.max_depth = max_depth
        self.tasks = self._load_runners(self.basedir, 0)

    def execute(self, tasks=None, depth=0):
        if tasks is None:
            tasks = self.tasks
        for n, t in tasks:
            log.info("%s %s" % ("*" * (depth+1), n))
            if isinstance(t, list):
                self.execute(tasks=t, depth=depth+1)
            else:
                t.execute()
    
    def _load_runners(self, path, depth):
        if depth > self.max_depth:
            raise RuntimeError("Exceeded maximum stage recursion depth.")
        tasks = []
        for name in sorted(os.listdir(path)):
            if os.path.isdir(name):
                subdir = os.path.join(path, name)
                tasks.append((name, self._load_runners(subdir, depth+1)))
            elif os.path.isfile(os.path.join(path, name)):
                if not name.endswith(".gd"):
                    continue
                fn = os.path.join(path, name)
                match = self.FNAME_PATTERN.match(name)
                if match:
                    name = match.group(2)
                tasks.append((name, TaskFile(fn, self.cfg, depth+1)))
        return tasks
