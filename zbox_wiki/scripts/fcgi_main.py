#!/usr/bin/env python

if __name__ == "__main__":
    import conf
    from zbox_wiki.main import web, Robots, SpecialWikiPage, WikiPage, mapping

    app = web.application(mapping, locals())

    web.wsgi.runwsgi = lambda func, addr=None: web.wsgi.runfcgi(func, addr)
    app.run()
