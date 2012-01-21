# About ZBox Wiki

ZBox(pronounce |ziːbɒks|) Wiki is a lightweight wiki system write in Python,  
it's released under the MIT license.

## FEATURES

What is **the most difference** between ZBox Wiki and others?

 * **pythonic**, lightweigt, simple, easy to **use**, easy to **read** and easy to **extend**
 * support Markdown (with table parsing extension) syntax, [guide](markdown-in-zboxwiki)
 * support button mode path
 * support simple TeX/LaTeX (requires [LaTeX] [latex] and [dvipng] [dvipng]), [demo](tex-in-zboxwiki)
 * support simple Graphviz/dot (requires [PyGraphviz] [pygraphviz]), [demo](dot-in-zboxwiki)

others

 * run up without database
 * IP/network range access restriction, simple ACL
 * auto generate the Table Of Content
 * auto include static file, support custom specify page(s) theme


## GET STARTED

### RUNTIME REQUIREMENTS I

Mac OS X, Debian GNU/Linux and Ubuntu includes Python 2.6+ by default;


Install GitHub(Git GUI client) on Mac OS X:

    http://mac.github.com/

Install git-core(Git CLI client) on Mac OS X:

    sudo port isntall git-core


Install Git on Debian GNU/Linux and Ubuntu:

    sudo apt-get install git-core -y


Install ZBox wiki:

    git clone git://github.com/shuge/zbox_wiki.git
    cd zbox_wiki
    python debug_main.py 8080

Visit [http://localhost:8080](http://localhost:8080) .


If you want to run it in instance mode:

    zwadmin.py create /path/to/proj
    zwd.py --path /path/to/proj


### RUNTIME REQUIREMENTS II (OPTIONAL)

Simple TeX/LaTeX feature requires:

 - latex
 - dvipng 1.13+


Install latex On Mac OS X, see [TexShop] [texshop] ;

Install dvipng on Mac OS X via MacPorts

    sudo port install dvipng


Install TeX/LaTeX (160 M +) on Debian/Ubuntu

    sudo apt-get install texlive-latex-base

Install dvipng on Debian/Ubuntu

    sudo apt-get install dvipng


### RUNTIME REQUIREMENTS III (OPTIONAL)

Simple Graphviz/dot feature requires:

 - pygraphviz


Install pygraphviz On Mac OS X via MacPorts

    sudo port install py27-pygraphviz


Install pygraphviz (20 M +) on Debian/Ubuntu

    sudo apt-get python-pygraphviz


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
