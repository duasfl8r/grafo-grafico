# -*- encoding: utf-8 -*-

VERSION = "0.1dev"

LOGFILE = 'graph_generator.log'

DEFAULT_EDGE_COLOR = '#000000'
"""
Color of the edges when not configured.
"""

BORDER_VALUE_OFFSET = -0.4
"""
Offset applied to the node's fill color value ("brightness") when calculating the border color.
"""

GRAPHVIZ_OPTIONS = {
    'graph': {
        # Do not make nodes overlap each other
        'overlap': 'false',

        # Puts nodes over edges in the final picture
        'outputorder': 'edgesfirst',

        # Background color -- RGB hex color or the special value 'transparent'
        'bgcolor': 'transparent',

        # Size of the picture in inches
        'size': '8x6',
    },
    'edge': {
    },
    'node': {
        # Fills nodes with color
        'style': 'filled',

        # This forces Graphviz to use the provided diameter sizes for
        # nodes, instead of calculating them based on the picture size.
        'fixedsize': 'true',
    },
}
"""
These options are passed on to Graphviz file.
See http://www.graphviz.org/doc/info/attrs.html for documentation.
"""
