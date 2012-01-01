# Demo Graphviz/dot in ZBox Wiki


----

```{{{#!dot
digraph G {
    rankdir = "LR"

    PyGraphviz[ URL = "http://networkx.lanl.gov/pygraphviz" ]

    ZBoxWiki[
        URL = "http://wiki.shuge-lab.org"
        fontcolor = "red"
    ]

    PyGraphviz -> ZBoxWiki
}
}}}
```

{{{#!dot
digraph G {
    rankdir = "LR"

    PyGraphviz[ URL = "http://networkx.lanl.gov/pygraphviz" ]

    ZBoxWiki[
        URL = "http://wiki.shuge-lab.org"
        fontcolor = "red"
    ]

    PyGraphviz -> ZBoxWiki
}
}}}

----


```{{{#!dot
digraph arch {
    rankdir = "LR"

    webpy [ label = "Web.py" ]
    py [ label = "Python" ]
    zbwiki [ label = "ZBoxWiki" ]

    webpy -> py
    zbwiki -> webpy
    
    Markdown -> zbwiki
    Graphviz -> zbwiki
    TeX -> zbwiki
}
}}}
```

{{{#!dot
digraph arch {
    rankdir = "LR"

    webpy [ label = "Web.py" ]
    py [ label = "Python" ]
    zbwiki [ label = "ZBoxWiki" ]

    webpy -> py
    zbwiki -> webpy
    
    Markdown -> zbwiki
    Graphviz -> zbwiki
    TeX -> zbwiki
}
}}}