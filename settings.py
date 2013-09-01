import random

SETTINGS = {
    'groups': [
        {
            'basecolor': (255, 0, 0),
        },
        {
            'basecolor': (0, 255, 0),
        },
        {
            'basecolor': (0, 0, 255),
        },
    ],
    'group': {
        'number_of_nodes': 30,
        'nodes_with_extralinks': 3,
        'intralinks_per_node': lambda: round(random.gauss(5, 3)),
        'extralinks_per_node': lambda: round(random.gauss(0.5, 1)),
    },
    'graphviz': {
        'graph': {
            'overlap': 'false',
            'outputorder': 'edgesfirst',
        },
        'node': {
            'style': 'filled',
            'regular': 'true',
        },
    },
}

def eval_setting(setting):
    if hasattr(setting, '__call__'):
        return setting()
    return setting

def get_setting(name, subsettings=None):
    if subsettings == None:
        subsettings = SETTINGS

    path = name.split('.')
    for part in path:
        if isinstance(subsettings, dict):
            if part in subsettings:
                subsettings = subsettings[part]
            else:
                return None
        elif isinstance(subsettings, (list, tuple)):
            index = int(part)
            return subsettings[index]
        else:
            return None

    return eval_setting(subsettings)
