#!/usr/bin/env python
from distutils.core import setup

short_desc = "a lightweight wiki system with Markdown/Graphviz/LaTeX support"

setup(
    name = "zbox_wiki",
    description = short_desc,
    long_description = "ZBox Wiki is %s, it's easy to use, easy to read and easy to extend.",
    
    version = "201201",
    
    author = "Shuge Lee",
    author_email = "shuge.lee@gmail.com",
    
    url = "https://github.com/shuge/zbox_wiki",
    
    license = "MIT License",
    
    platforms = ["Mac OS X"],


    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers = [
        "Development Status :: 4 - Beta",
        "Environment :: MacOS X",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 2 :: Only",
        "Topic :: Text Processing",
        ],
    
    
    packages = ["zbox_wiki", "zbox_wiki.commons"],
    package_data = {
      "zbox_wiki" : [
          "templates/*.tpl",
          "static/css/*.css",
          "static/js/*.js",
          "static/js/prettify/*.js",
          "static/js/prettify/*.css",
          "pages/robots.txt",
          "pages/zbox-wiki/*.md",
          ],
    },

    scripts = [
        "scripts/zwadmin.py",
        "scripts/zwd.py",
    ],
    
    
    
)