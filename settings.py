import random

SETTINGS = {
    'groups': [
        {
            'basecolor': (142, 76, 211),
            'brightness_offset': lambda: round(random.gauss(20, 30)),
        },
        {
            'basecolor': (60, 60, 156),
            'brightness_offset': lambda: round(random.gauss(20, 30)),
        },
        {
            'basecolor': (156, 60, 115),
            'brightness_offset': lambda: round(random.gauss(20, 30)),
        },
        {
            'basecolor': (120, 76, 200),
            'brightness_offset': lambda: round(random.gauss(20, 30)),
        },
        {
            'basecolor': (50, 70, 156),
            'brightness_offset': lambda: round(random.gauss(20, 30)),
        },
        {
            'basecolor': (150, 55, 130),
            'brightness_offset': lambda: round(random.gauss(20, 30)),
        },
        {
            'basecolor': (180, 55, 120),
            'brightness_offset': lambda: round(random.gauss(20, 30)),
        },
    ],
    'group': {
        'number_of_nodes': 30,
        'nodes_with_extralinks': 3,
        'intralinks_per_node': lambda: max(1, round(random.gauss(5, 3))),
        'extralinks_per_node': lambda: max(1, round(random.gauss(0.5, 1))),
    },
    'graphviz': {
        'graph': {
            'overlap': 'false',
            'outputorder': 'edgesfirst',
            'bgcolor': '"#3C5F9C"',
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
