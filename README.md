Grafo-gráfico: arte como grafo, grafo como arte
===============================================

![Exemplo](https://raw.github.com/lucastx/grafo-grafico/master/exemplo.png)

Gera imagens de grupos de grafos intra e extra-ligados --
uma visualização artística de organizações P2P.

O script `graph_generator.py` gera uma descrição de um grafo -- uma lista de
nós e links entre eles -- no formato do Graphviz, um conjunto de ferramentas
de visualização de grafos.

A ferramenta `fdp` do Graphviz gera então uma bonita visualização do grafo.

Segundo o manual do Graphviz:

> fdp desenha grafos não-direcionados usando um modelo de "mola". Ele se
> baseia na estratégia direcionada-a-forças, no espírito de Fruchterman e
> Reingold.

Esse projeto está licenciado sob GNU GPLv3 ou superior -- os termos da
licença estão em `LICENSE.txt`.

Dependências
------------

- Python 2.7 ou 3.x
- [Graphviz][graphviz]

[graphviz]: http://graphviz.org/

Configurando
------------

Copie a configuração de exemplo `config-dist.py` pra `config.py`, e altere
como quiser -- as opções estão levemente documentadas.

Usando
------

### Com o make

```bash
make build
```

### Manualmente

```bash
python graph_generator.py > grafo.gv
```

Geramos então a imagem final usando a ferramenta `fdp` do Graphviz:

```bash
fdp -Tpng -o grafo.png grafo.gv
```
