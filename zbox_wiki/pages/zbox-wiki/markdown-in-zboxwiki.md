# A Short Guide For Markdown

> Markdown is intended to be as easy-to-read and easy-to-write as is feasible.

http://daringfireball.net/projects/markdown/syntax#philosophy


## Inline/Span Elements

### bold, italic

source:

    a **fat boy**, a _thin girl_


HTML:

a **fat boy**, a _thin girl_


### Link

source:

```
This is [Wikipedia](http://en.wikipedia.org/wiki) link.
```


HTML:

This is [Wikipedia](http://en.wikipedia.org/wiki) HTML link.


### Reference-style Link

source:

```
This is [Wikipedia] [wp] link.

This is another [Wikipedia in English] [wp] link.

[wp]: http://en.wikipedia.org/wiki
```


HTML:

This is [Wikipedia] [wp] link.

This is another [Wikipedia in English] [wp] link.

[wp]: http://en.wikipedia.org/wiki


### Image

source:

```
![Alt text](/path/to/img.jpg "Optional title")
```



## Block Elements


### Header/Title

source:

```
# header level 1
## header level 2
### header level 3
#### header level 4
##### header level 5
```


### Source Code I

Inline source code.


source:

```
it prints `hello world`.
```


HTML:

it prints `hello world`


### Source Code II

Multiple line source code.

source:

    ```
    int
    main(void)
    {
        printf("hello");
        return 0;
    }
    ```

      
HTML:

```
int 
main( void )
{
    printf( "hello" );
    return 0;
}
```


### Table

source:

|| name || desc ||
| SIP | Session Initial Protocol |
| SIP-C | Session Initial Protocol compact version |


### Macro

Graphviz/dot

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


TeX/LaTeX

```{{{#!tex
\frac{\alpha^{\beta^2}}{\delta + \alpha}
}}}
```


## References

For more syntax candy, see http://daringfireball.net/projects/markdown/syntax