# -*- encoding: utf-8 -*-

import random

CONFIG = {
    'groups': [
        {
            'basecolor': '#0d4100',
            'brightness_offset': lambda: random.gauss(0, 0.2),
            'node_diameter': lambda: random.gauss(10, 2),
        },
        {
            'basecolor': '#00706e',
            'brightness_offset': lambda: random.gauss(0, 0.2),
            'node_diameter': lambda: random.gauss(15, 3),
        },
        {
            'basecolor': '#8c6700',
            'brightness_offset': lambda: random.gauss(0, 0.2),
            'node_diameter': lambda: random.gauss(13, 3),
        },
    ],

    'group': {
        'number_of_nodes': 15,
        'nodes_with_extralinks': 4,
        'intralinks_per_node': lambda: max(1, round(random.gauss(13, 2))),
        'extralinks_per_node': lambda: max(1, round(random.gauss(5, 1))),
    },

    'graphviz': {
        'graph': {
            'overlap': 'false',
            'outputorder': 'edgesfirst',
            'bgcolor': 'transparent',
            'size': '10,10',
        },
        'node': {
            'style': 'filled',
            'fixedsize': 'true',
        },
    },
}
