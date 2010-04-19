import inspect
import logging
import optparse as op
import os
import sys

import api
import attrdict
import odict

LOG_LEVELS = {
    "critical": logging.CRITICAL,
    "error": logging.ERROR,
    "warning": logging.WARNING,
    "info": logging.INFO,
    "debug": logging.DEBUG
}

log = logging.getLogger(__name__)

__usage__ = "%prog [OPTIONS] [BASE_DIRECTORY]"

def options():
    return [
        op.make_option('-c', '--cfg', dest='cfg', metavar='FILE',
            help='Path to a config file to load. [./godo.cfg.py]'),
        op.make_option('--log-file', dest='logfile', metavar='FILE',
            help='Log output destination. [stdout]'),
        op.make_option('--log-level', dest='loglevel', metavar='STRING',
            help='Minimum log level severity. [info]'),
        op.make_option('-T', '--trace', dest='trace', default=False,
            action='store_true',
            help='Show exception tracebacks on error.'),
    ]

def run():
    # Unbuffer stdout
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)
    
    parser = op.OptionParser(usage=__usage__, option_list=options())
    opts, args = parser.parse_args()

    if len(args) > 1:
        parser.error("Unknown arguments: %s" % " ".join(args))
 
    configure_logging(opts)

    basedir = args[0] if len(args) else os.getcwd()

    if opts.trace:
        log.info("Loading configuration.")

    cfgfname = os.path.join(basedir, "godo.cfg.py")
    if opts.cfg or os.path.isfile(cfgfname):
        if opts.cfg:
            cfgfname = opts.cfg
        cfg = load_config(cfgfname)
    else:
        cfg = attrdict.attrdict()

    if opts.trace:
        log.info("Loading task definitions.")

    tasklist = []
    for path, dnames, fnames in os.walk(basedir):
        # Not sure if this sort is strictly necessary
        # but it can affect ordering as shown by adding
        # reverse=True.
        dnames.sort()
        for fname in sorted(fnames):
            if not fname.endswith(".gd"):
                continue
            fname = os.path.join(path, fname)
            for (name, func) in load_tasks(fname):
                tasklist.append((name, path, func))

    if opts.trace:
        log.info("Executing.")

    for (name, path, func) in tasklist:
        if opts.trace:
            log.info("")
            log.info("%s %s %s" % ("==", name, "=="))
            log.info("")
        try:
            arity = len(inspect.getargspec(func)[0])
            with api.cd(path):
                if arity == 1:
                    func(cfg)
                else:
                    func()
        except Exception, inst:
            if opts.trace:
                log.exception("Error in task: %s" % name)
            else:
                log.error("Error in task %s:\n    %s" % (name, str(inst)))
            sys.exit(1)

    if opts.trace:
        log.info("")
        log.info("Finished.")

def load_config(fname):
    g = {
        "__builtins__": __builtins__,
        "__file__": fname,
        "__name__": None,
        "__package__": None
    }
    ret = attrdict.attrdict()
    execfile(fname, g, ret)
    for k, v in ret.iteritems():
        if inspect.isfunction(v):
            v.func_globals.update(ret)
    return ret

def load_tasks(fname):
    defs = odict.odict()
    execfile(fname, mk_globals(fname), defs)
    for name, func in defs.iteritems():
        if not callable(func) or not getattr(func, "__task__", False):
            continue
        if len(inspect.getargspec(func)[0]) > 1:
            raise ValueError("Invalid task function arity: %s" % name)
        func.func_globals.update(defs)
        yield name, func

def mk_globals(fname):
    return {
        "__builtins__": __builtins__,
        "__file__": fname,
        "__name__": None,
        "__package__": None,
        "task": api.task,
        "cd": api.cd,
        "run": api.run,
        "sudo": api.sudo
    }

def configure_logging(opts):
    handlers = []
    if opts.logfile:
        handlers.append(logging.FileHandler(opts['logfile']))
    else:
        handlers.append(logging.StreamHandler())

    loglevel = (opts.loglevel or "info").lower()
    loglevel = LOG_LEVELS.get(loglevel, logging.INFO)
    log.setLevel(loglevel)
    format = r"%(message)s"
    for h in handlers:
        h.setFormatter(logging.Formatter(format))
        log.addHandler(h)
