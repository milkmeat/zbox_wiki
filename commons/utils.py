#!/usr/bin/env python
import os
import web

__all__ = [
    "cat"
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

if __name__ == "__main__":
    import doctest
    doctest.testmod()
