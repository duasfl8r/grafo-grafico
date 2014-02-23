# -*- encoding: utf-8 -*-

"""
Configurações do grafo-grafico.

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
"""

import random

CONFIG = {
    # Lista de grupos e suas opções específicas
    'groups': [
        {
            # Cor base dos nós do grupo
            'basecolor': '#8e4cd3',
            # Variação do brilho pra cada nó específico -- altera o
            # 'value' da imagem convertida em HSV
            #
            # Mexa no segundo parâmetro pra alterar a amplitude de
            # variação de tons.
            'brightness_offset': lambda: random.gauss(0, 0.2),

            # Diâmetro base dos nós do grupo, em polegadas (inches)
            'base_diameter': 1,
            # Variação do diâmetro pra cada nó específico
            'diameter_offset': lambda: random.gauss(0, 0.2),
        },
        {
            'basecolor': '#3c3c9c',
            'brightness_offset': lambda: random.gauss(0, 0.2),
            'base_diameter': 1,
            'diameter_offset': lambda: random.gauss(0, 0.2),
        },
        {
            'basecolor': '#9c3c73',
            'brightness_offset': lambda: random.gauss(0, 0.2),
            'base_diameter': 1,
            'diameter_offset': lambda: random.gauss(0, 0.2),
        },
        {
            'basecolor': '#5a82c8',
            'brightness_offset': lambda: random.gauss(0, 0.2),
            'base_diameter': 1,
            'diameter_offset': lambda: random.gauss(0, 0.2),
        },
    ],
    # Opções pra todos os grupos
    'group': {
        # Número de nós pra cada grupo
        'number_of_nodes': 30,
        # Número de nós com links intergrupos
        'nodes_with_extralinks': 4,
        # Número de intralinks -- links pra nós do mesmo grupo -- de um # nó
        'intralinks_per_node': lambda: max(1, round(random.gauss(15, 3))),
        # Número de interlinks -- links pra nós de outro grupo -- de um # nó
        'extralinks_per_node': lambda: max(1, round(random.gauss(2, 2))),
    },
    # Opções repassadas pro arquivo GV do graphviz
    'graphviz': {
        'graph': {
            'overlap': 'false',
            'outputorder': 'edgesfirst',
            'bgcolor': '#3C5F9C',
        },
        'node': {
            'style': 'filled',
            'regular': 'true',
            'fixedsize': 'true',
        },
    },
}
