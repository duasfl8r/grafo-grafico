import random

SETTINGS = {
    'graph': {
        'number_of_groups': 3,
    },
    'group': {
        'number_of_nodes': 30,
        'nodes_with_extralinks': 3,
        'intralinks_per_node': lambda: round(random.gauss(5, 3)),
        'extralinks_per_node': lambda: round(random.gauss(0.5, 1)),
    },
}

def eval_setting(setting):
    if hasattr(setting, '__call__'):
        return setting()
    return setting

def get_setting(name):
    path = name.split('.')
    subsettings = SETTINGS
    for part in path:
        if part in subsettings:
            subsettings = subsettings[part]
        else:
            return None
    return eval_setting(subsettings)
