#!/usr/bin/env python
import codecs
import os
import shlex
import subprocess
import web

__all__ = [
    "cat",
    "strip_bom",
    "which",
    "run",
]


def cat(*args):
    buf = ""
    for i in args:
        full_path = web.safeunicode(i)
        if os.path.isfile(full_path):
            f = file(full_path)
            buf = "%s%s" % (buf, f.read().strip())
            f.close()

    return web.safeunicode(buf)

def strip_bom(text):
    if web.safestr(text[0]) == codecs.BOM_UTF8:
        text = text[1:]

    return text

def which(name):
    bin_paths = (
        "/usr/bin", # APT on Debian
        "/opt/local/bin", # PortsMac on Mac OS X
        )

    for i in bin_paths:
        full_path = os.path.join(i, name)
        if os.path.exists(full_path):
            return full_path


def run(cmd):
    args = shlex.split(cmd)
    try:
        p_obj = subprocess.Popen(args, stdout = subprocess.PIPE, shell = True)
#        resp = p_obj.stdout.read().strip("\n")
        resp = p_obj.stdout.read()
    except TypeError:
        resp = None

    if not resp:
#        resp = os.popen(cmd).read().strip().split('\n')
        resp = os.popen(cmd).read().strip()

    resp = web.rstrips(resp, "\n")

    resp = web.safeunicode(resp)

    return resp



if __name__ == "__main__":
    import doctest
    doctest.testmod()

    import sys
    if sys.platform == "darwin":
        print repr(run("uname -s"))
        assert run("uname -s") in ("Darwin", "Linux")
