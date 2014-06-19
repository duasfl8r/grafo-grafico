# -*- encoding: utf-8 -*-

import random

# Documentação extensa sobre uso de funções e especificação de cores lá
# embaixo.
CONFIG = {
    # Lista de grupos e suas opções específicas
    'groups': [
        {
            # Cor base dos nós do grupo
            'basecolor': '#8e4cd3',

            # Variação do brilho pra cada nó específico -- altera o
            # 'value' da imagem convertida em HSV.
            #
            # Mexa no segundo parâmetro pra alterar a amplitude de
            # variação de tons.
            'brightness_offset': lambda: random.gauss(0, 0.2),

            'node_diameter': lambda: random.gauss(1, 0.5),

            # Número de nós do grupo
            'number_of_nodes': 30,

            # Número de intralinks -- links pra nós do mesmo grupo -- de um nó
            'intralinks_per_node': lambda: max(1, round(random.gauss(15, 3))),
            # Número de nós com links intergrupos
            'nodes_with_extralinks': 4,

            # Número de interlinks -- links pra nós de outro grupo -- de um # nó
            'extralinks_per_node': lambda: max(1, round(random.gauss(2, 2))),
        },
        {
            'basecolor': '#3c3c9c',
            'brightness_offset': lambda: random.gauss(0, 0.2),
            'node_diameter': lambda: random.gauss(0.2, 0.1),
            'number_of_nodes': 50,
            'intralinks_per_node': lambda: max(1, round(random.gauss(15, 3))),
            'nodes_with_extralinks': 4,
            'extralinks_per_node': lambda: max(1, round(random.gauss(2, 2))),
        },
        {
            'basecolor': '#9c3c73',
            'brightness_offset': lambda: random.gauss(0, 0.2),
            'node_diameter': lambda: random.gauss(3, 1),
            'number_of_nodes': 15,
            'intralinks_per_node': lambda: max(1, round(random.gauss(15, 3))),
            'nodes_with_extralinks': 4,
            'extralinks_per_node': lambda: max(1, round(random.gauss(2, 2))),
        },
        {
            'basecolor': '#5a82c8',
            'brightness_offset': lambda: random.gauss(0, 0.2),
            'node_diameter': lambda: random.gauss(1, 0.2),
            'number_of_nodes': 10,
            'intralinks_per_node': lambda: max(1, round(random.gauss(15, 3))),
            'nodes_with_extralinks': 4,
            'extralinks_per_node': lambda: max(1, round(random.gauss(2, 2))),
        },
    ],

    # Opções repassadas pro arquivo GV do graphviz
    'graphviz': {
        'graph': {
            # Não permite que os nós fiquem um por cima dos outros --
            # torna o resultado final mais bonito,
            # na *minha* opinião ;-)
            'overlap': 'false',

            # Impede que as arestas fiquem por cima dos nós
            'outputorder': 'edgesfirst',

            # Cor de fundo, ou 'transparent'
            'bgcolor': 'transparent',
            'size': '8x6',
        },
        'node': {
            # Remover essa opção faz os nós terem só o contorno e as
            # arestas visíveis -- sem preenchimento.
            'style': 'filled',

            # Faz as configurações de diâmetro de nó funcionarem -- não
            # calcula um tamanho 'ótimo' pros nós a partir do tamanho da
            # tela.
            'fixedsize': 'true',
        },
    },
}

"""
Configurações do grafo-grafico.

Como as configurações são acessadas
-----------------------------------

Dentro do grafo-grafico, uma configuração acessada com:

    cfg('groups.0.base_color')

Equivale a acessar o valor de `CONFIG` dessa forma:

    CONFIG['groups'][0]['base_color']

Se o valor retornado por esse acesso for uma função, ele é então
invocado como tal e o valor retornado se torna o valor da configuração
naquele dado acesso.

Num próximo acesso à mesma configuração, a função é novamente invocada e
um novo valor retornado.

Isso permite que a configuração retorne valores aleatórios, ou usando uma
distribuição estatística.

Cores
-----

Versão resumida: As cores devem ser especificadas em RGB, no formato "#FFFFFF", com todos
os seis algarismos.

Detalhes sórdidos:

Algumas configurações de cores são manipuladas internamente pelo
grafo-grafico -- essas devem ser *mesmo* especificadas no formato acima.

Outras são repassadas diretamente pro graphviz, sendo então possível
definir as cores em qualquer um dos formatos especificados aqui:

http://www.graphviz.org/doc/info/attrs.html#k:color
"""