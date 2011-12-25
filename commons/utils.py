#!/usr/bin/env python
import os
import shlex
import subprocess
import web

__all__ = [
    "cat",
    "which",
    "run",
]


def cat(*args):
    buf = ""
    for i in args:
        fullpath = web.safeunicode(i)
        if os.path.isfile(fullpath):
            f = file(fullpath)
            buf = "%s%s" % (buf, f.read().strip())
            f.close()

    return web.safeunicode(buf)


def which(name):
    bin_paths = (
        "/usr/bin", # APT on Debian
        "/opt/local/bin", # PortsMac on Mac OS X
        )

    for i in bin_paths:
        fullpath = os.path.join(i, name)
        if os.path.exists(fullpath):
            return fullpath


def run(cmd):
    args = shlex.split(cmd)
    p_obj = subprocess.Popen(args, stdout = subprocess.PIPE, shell = True)
    resp = p_obj.stdout.read().strip()
    return resp



if __name__ == "__main__":
    import doctest
    doctest.testmod()

    assert run("uname -s") in ("Darwin", "Linux")