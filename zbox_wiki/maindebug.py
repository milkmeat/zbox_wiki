#!/usr/bin/env python
import os
import conf
import main

zbox_wiki = main

zbox_wiki.commons.tex2png.DEBUG = True

#zbox_wiki_path = zbox_wiki.__path__[0]
zbox_wiki_path = conf.PWD

conf.pages_path = os.path.realpath(os.path.join(conf.PWD, "other_pages"))
conf.static_path = os.path.join(zbox_wiki_path, "static")
conf.templates_path = os.path.join(zbox_wiki_path, "templates")

zbox_wiki.start()
