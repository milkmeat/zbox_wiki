#!/usr/bin/env python
import os
import conf
import commons

commons.tex2png.DEBUG = True


other_pages_path = os.path.join(conf.PWD, "other_pages")
if os.path.exists(other_pages_path):
    conf.pages_path = other_pages_path

    page_link_in_static_path = os.path.join(conf.PWD, "static", "pages")
    if not os.path.exists(page_link_in_static_path):
        os.symlink(other_pages_path, page_link_in_static_path)

import main
main.fix_folders()
main.app.run()
