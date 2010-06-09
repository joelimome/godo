import inspect
import logging
import optparse as op
import os
import sys

import api
import attrdict
import task

__usage__ = "%prog [OPTIONS] [BASE_DIRECTORY]"

def options():
    return [
        op.make_option('-c', '--cfg', dest='cfg', metavar='FILE',
            help='Path to a config file to load. [./godo.cfg.py]'),
        op.make_option('-l', dest='lib', metavar='DIR',
            help="Add a DIR to the Python path."),
        op.make_option('--log-file', dest='logfile', metavar='FILE',
            help='Log output destination. [stdout]'),
        op.make_option('--log-level', dest='loglevel', metavar='STRING',
            help='Minimum log level severity. [info]')
    ]

def run():
    # Unbuffer stdout
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)
    
    parser = op.OptionParser(usage=__usage__, option_list=options())
    opts, args = parser.parse_args()

    if len(args) > 1:
        parser.error("Invalid arguments: %s" % " ".join(args))

    basedir = args[0] if len(args) else os.getcwd()
    
    if opts.lib is not None:
        sys.path.insert(0, opts.lib)
    else:
        libdir = os.path.join(basedir, "lib")
        if os.path.isdir(libdir):
            sys.path.insert(0, libdir)
    
    configure_logging(opts)
    cfg = load_config(basedir, opts.cfg)
    mgr = task.TaskManager(cfg, basedir)
    mgr.execute()

def configure_logging(opts):
    if opts.logfile:
        handler = logging.FileHandler(opts['logfile'])
    else:
        handler = logging.StreamHandler()

    format = r"%(message)s"
    handler.setFormatter(logging.Formatter(format))
    logging.getLogger().addHandler(handler)

    levels = {
        "critical": logging.CRITICAL,
        "error": logging.ERROR,
        "warning": logging.WARNING,
        "info": logging.INFO,
        "debug": logging.DEBUG
    }

    levelname = (opts.loglevel or "info").lower()
    loglevel = levels.get(levelname, logging.INFO)
    logging.getLogger().setLevel(loglevel)

def load_config(basedir, fname):
    default = os.path.join(basedir, "godo.cfg.py")
    cfgname = None
    if fname and os.path.isfile(fname):
        cfgname = fname
    elif os.path.isfile(default):
        cfgname = default
    ret = attrdict.attrdict()
    if cfgname is not None:
        ret.update({
            "__builtins__": __builtins__,
            "__file__": os.path.basename(cfgname),
            "__name__": None,
            "__package__": None
        })
        execfile(cfgname, ret, ret)
    return ret

def load_stages(basedir, cfg):
    stages = []
    for path, dnames, fnames in os.walk(basedir):
        dnames.sort()
        for fname in sorted(fnames):
            if not fname.endswith(".gd"):
                continue
            fname = os.path.join(path, fname)
            stages.append(stage.Stage(basedir, fname, cfg))
    return stages
