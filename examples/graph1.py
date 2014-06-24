# -*- encoding: utf-8 -*-

"""
Configurations of a graph.

Each final value can really be any python code.
If the value is callable (i.e. a function), the function is called and its return value is the value of the option.
This allows nondeterministic (e.g. random) values.

More information on the way this is made on `graph_generator.cfg` docstring.

Colors must be specified as a RGB hex value (e.g. "#ff0000").
"""

import random

CONFIG = {
    # A list of the groups and its specific options.
    'groups': [
        {
            # Base color of the nodes
            'basecolor': '#8e4cd3',

            # Brightness offset for each specific node -- changes the
            # 'value' parameter of the color when converted to HSV.
            #
            # Tweak the second parameter to change the amplitude of the
            # tone variation.
            'brightness_offset': lambda: random.gauss(0, 0.2),

            'node_diameter': lambda: random.gauss(1, 0.5),
            'number_of_nodes': 30,

            # Intralinks -> edges between nodes of the SAME group
            'intralinks_per_node': lambda: max(1, round(random.gauss(15, 3))),

            # Extralinks -> edges between nodes of DIFFERENT groups
            'nodes_with_extralinks': 4,
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


    # Options for the edges
    'edge': {
        # Color of the edges -- the special value 'average_nodes'
        # averages the fill color of the nodes.
        'color': 'average',
    },
}
