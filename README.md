# About ZBox Wiki

ZBox Wiki is a lightweight wiki system implement in Python and web framework [web.py](http://webpy.org/).

ZBox Wiki doesn't uses any databases, you can edit page files via 

- Firefox + It's All Text! + Emacs/gVIM online
- Emacs/gVIM offline


## GET STARTED

To get the latest development version from git:

    git clone git@github.com:shuge/zbox_wiki.git
    cd zbox_wiki
    python main.py
    
Visit http://localhost:8080 .

## FEATURES

- it really works
- run up without database, CRUD page file
- support [Markdown](http://daringfireball.net/projects/markdown/) (with table parsing extension) syntax
- auto include static image file
- auto generate table of content
- list all page files (implement in GNU findutils)
- list recent changed page files (implement in GNU findutils)
- search by file name and file content (implment in GNU findutils and GNU grep)
- support simple TeX/LaTeX (requires [LaTeX] [latex] and [dvipng] [dvipng])
- support button mode path
- IP/network range access restriction

## RUNTIME REQUIREMENTS

- python 2.6+

    On Mac OS X via MacPorts, `sudo port install python26`

- web.py 0.37+

    If you install it by `easy_install web.py`,
    you have to fix [issue #95](https://github.com/webpy/webpy/issues/95) by manual.

    Strong recommend you install it from latest source:

        git clone https://github.com/webpy/webpy.git
        cd webpy.git
        sudo python setup.py install

- py-markdown 2.0.3+

    On Mac OS X via MacPorts, `sudo port install py-markdown`

## SCREENSHOTS

 - Auto generate table of content and highlight 
 - List page files in tree
 - Simple search
 - Button-mode path

http://www.flickr.com/photos/71317153@N06/6445429383/in/set-72157628256603985/


[latex]: http://www.tug.org/texlive
[dvipng]: http://savannah.nongnu.org/projects/dvipng
