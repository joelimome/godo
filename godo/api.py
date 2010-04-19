
import os
from subprocess import Popen, PIPE

class CommandExecutionError(Exception):
    def __init__(self, cmd, rcode, stdout, stderr):
        self.cmd = cmd
        self.rcode = rcode
        self.stdout = stdout
        self.stderr = stderr

    def __str__(self):
        return ''.join([
            "Error running command:",
            "",
            "    %s" % self.cmd,
            "    Exited with: %s" % self.rcode,
            "",
            "STDOUT:",
            "=======",
            self.stdout,
            "",
            "STDERR:",
            "=======",
            self.stderr
        ])

def task(func):
    func.__task__ = True
    return func

class cd(object):
    def __init__(self, path):
        self.cwd = None
        self.path = path
    def __enter__(self):
        self.cwd = os.getcwd()
        os.chdir(self.path)
    def __exit__(self, exc_typ, exc_inst, exc_tb):
        os.chdir(self.cwd)
        return False

def run(cmd, input=None):
    pipe = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
    (stdout, stderr) = pipe.communicate(input=input)
    if pipe.wait() != 0:
        raise CommandExecutionError(cmd, pipe.returncode, stdout, stderr)
    return stdout

def sudo(cmd, input=None):
    return run("sudo " + cmd, input=input)
