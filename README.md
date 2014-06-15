Grafo-gráfico
=============

Art as graph, graph as art
--------------------------


![Example](https://raw.github.com/lucastx/grafo-grafico/master/examples/grafo.png)

Generates image of graph groups intralinked and extralinked -- an artistic
visualization of P2P patterns and organizations.

The `graph_generator.py` script builds a description of a graph -- a list of
nodes and the links between them -- in a format [Graphviz][graphviz] accepts.
The `fdp` tool then creates a beautiful visualization of the graph
descripted.

According to Graphviz man page:

> fdp  draws undirected graphs using a ``spring'' model. It relies on a
force‐directed approach in the spirit  of  Fruchterman  and Reingold

This project is licensed under GNU GPLv3 or greater -- the terms of the
license are in `LICENSE.txt`.

Dependencies
------------

- Python 2.7 or 3.x
- [Graphviz][graphviz]

[graphviz]: http://graphviz.org/

Configuration
-------------

Copy the example configuration `config-dist.py` to `config.py`, and change
it as you will -- the file has documentation in comments.

Usage
-----

To generate a graph for the `examples/graph1.py` and save it on
`output.png`:

```bash
python cli.py --format=png --output=output.png generate examples/graph1.py
```

To stop at the intermediate Graphviz format -- a text file with instructions
to build a precise graph:

```bash
python cli.py --format=gv --output=output.gv generate examples/graph1.py
```
