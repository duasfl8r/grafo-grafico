import random

SETTINGS = {
    'groups': [
        {
            'basecolor': (142, 76, 211),
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
        {
            'basecolor': (120, 130, 190),
            'brightness_offset': lambda: round(random.gauss(0, 40)),
        },
        {
            'basecolor': (100, 100, 200),
            'brightness_offset': lambda: round(random.gauss(0, 40)),
        },
        {
            'basecolor': (130, 70, 200),
            'brightness_offset': lambda: round(random.gauss(0, 40)),
        },
        {
            'basecolor': (90, 70, 190),
            'brightness_offset': lambda: round(random.gauss(0, 40)),
        },
        {
            'basecolor': (142, 76, 211),
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
        {
            'basecolor': (120, 130, 190),
            'brightness_offset': lambda: round(random.gauss(0, 40)),
        },
        {
            'basecolor': (100, 100, 200),
            'brightness_offset': lambda: round(random.gauss(0, 40)),
        },
        {
            'basecolor': (130, 70, 200),
            'brightness_offset': lambda: round(random.gauss(0, 40)),
        },
        {
            'basecolor': (90, 70, 190),
            'brightness_offset': lambda: round(random.gauss(0, 40)),
        },
    ],
    'group': {
        'number_of_nodes': 30,
        'nodes_with_extralinks': 4,
        'intralinks_per_node': lambda: max(1, round(random.gauss(15, 3))),
        'extralinks_per_node': lambda: max(1, round(random.gauss(2, 2))),
    },
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

