# About ZBox Wiki

ZBox(pronounce |ziːbɒks|) Wiki is a lightweight wiki system write in Python and [web.py](http://webpy.org/),


it's released under the MIT license.

## FEATURES

What is **the most difference** between ZBox Wiki and others?

 * **pythonic**, lightweigt, simple, easy to **use**, easy to **read** and easy to **extend**
 * support Markdown (with table parsing extension) syntax, [guide](markdown-in-zboxwiki)
 * support button mode path
 * support simple TeX/LaTeX (requires [LaTeX] [latex] and [dvipng] [dvipng]), [demo](tex-in-zboxwiki)
 * support simple Graphviz/dot (requires [PyGraphviz] [pygraphviz]), [demo](dot-in-zboxwiki)

others

 * it really works
 * run up without database
 * IP/network range access restriction, simple ACL
 * auto generate the Table Of Content
 * auto include static file, support custom specify page(s) theme


## GET STARTED

### RUNTIME REQUIREMENTS I

ZBox Wiki run up requires:

 - Python 2.6+
 - web.py 0.37+
 - py-markdown 2.0.3+


Mac OS X and Debian/Ubuntu includes Python 2.6+ by default;


If you install web.py by `easy_install web.py`,
you have to fix [issue #95](https://github.com/webpy/webpy/issues/95) by manual.

Strong recommend you install it from latest source:

    git clone git://github.com/webpy/webpy.git
    cd webpy
    sudo python setup.py install


Install py-markdown on Mac OS X via MacPorts,

    sudo port install py-markdown

Install py-markdown on Debian/Ubuntu

    sudo aptitude install python-markdown


To get the latest development version ZBox wiki from git:

    git clone git://github.com/shuge/zbox_wiki.git
    cd zbox_wiki
    python maindebug.py 8080

Visit [http://localhost:8080](http://localhost:8080) .


### RUNTIME REQUIREMENTS II (OPTIONAL)

Simple TeX/LaTeX feature requires:

 - latex
 - dvipng 1.13+


Install latex On Mac OS X, see [TexShop] [texshop] ;

Install dvipng on Mac OS X via MacPorts

    sudo port install dvipng


Install TeX/LaTeX (160 M +) on Debian/Ubuntu

    sudo aptitude install texlive-latex-base

Install dvipng on Debian/Ubuntu

    sudo aptitude install dvipng


### RUNTIME REQUIREMENTS III (OPTIONAL)

Simple Graphviz/dot feature requires:

 - pygraphviz


Install pygraphviz On Mac OS X via MacPorts

    sudo port install py27-pygraphviz


Install pygraphviz (20 M +) on Debian/Ubuntu

    sudo aptitude python-pygraphviz


Graphviz GUI Editors on Mac OS X in MacPorts:

 * gvedit
 * graphviz-gui



## SCREENSHOTS

[screenshots on flickr](http://www.flickr.com/photos/71317153@N06/6445429383/in/set-72157628256603985/)



## A SHORT GUIDE FOR MARKDOWN


[A Short Guide For Markdown](markdown-in-zboxwiki)





[macports]: http://www.macports.org/install.php

[latex]: http://www.tug.org/texlive
[texlive]: http://www.tug.org/texlive
[texshop]: http://pages.uoregon.edu/koch/texshop

[dvipng]: http://savannah.nongnu.org/projects/dvipng

[pygraphviz]: http://networkx.lanl.gov/pygraphviz
