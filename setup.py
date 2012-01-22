#!/usr/bin/env python
from setuptools import setup

short_desc = "a lightweight wiki system with Markdown/Graphviz/LaTeX support"

kwargs = dict(
    name = "zbox_wiki",
    description = short_desc,
    long_description = "ZBox Wiki is %s, it's easy to use, easy to read and easy to extend." % short_desc,

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


    packages = [
        "zbox_wiki",
        "zbox_wiki.commons",
        "zbox_wiki.web",
        "zbox_wiki.markdown",
        ],
    
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

    install_requires = [
        # "markdown>=2.1.0",  there is a copy of Markdown-2.1.0 in zbox_wiki/commons/markdown
        "argparse"
    ],
)

setup(**kwargs)
