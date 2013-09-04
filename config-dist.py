# -*- encoding: utf-8 -*-

import random

"""
Configurações gerais.

Se um valor de configuração for uma função, a função será chamada cada
vez que a configuração for acessada.

Isso permite que a configuração retorne valores aleatórios, ou numa
distribuição estatística.

"""

CONFIG = {
    # Lista de grupos e suas opções específicas
    'groups': [
        {
            # Cor base dos nós do grupo, em HSV
            'basecolor': (142, 76, 211),
            # Variação do brilho pra cada nó específico
            #
            # Mexa no segundo parâmetro pra alterar a amplitude de
            # variação de tons.
            'brightness_offset': lambda: round(random.gauss(0, 40)),
        },
        {
            'basecolor': (60, 60, 156),
            'brightness_offset': lambda: round(random.gauss(0, 40)),
        },
        {
            'basecolor': (156, 60, 115),
            'brightness_offset': lambda: round(random.gauss(0, 40)),
        },
        {
            'basecolor': (90, 130, 200),
            'brightness_offset': lambda: round(random.gauss(0, 40)),
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
        },
    },
}
