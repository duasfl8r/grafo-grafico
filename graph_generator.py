# -*- encoding: utf-8 -*-

import sys
import random

try:
    from config import CONFIG
except ImportError:
    sys.stderr.write('Arquivo `config.py` não encontrado. Você já o copiou de `config-dist.py?`')
    sys.exit(-1)


from colors import rgb_to_hsv, hsv_to_rgb, hsv_change_brightness

class Graph:
    def __init__(self):
        self.nodes = set()
        self.graph_options = {}
        self.node_options = {}

    def graphviz(self):
        content = '\n'.join(node.graphviz() for node in self.nodes)

        graph_option_tuples = [(k, v) for k, v in self.graph_options.items()]
        graph_option_strs = ['{0}="{1}"'.format(k, v) for k, v in graph_option_tuples]

        node_option_tuples = [(k, v) for k, v in self.node_options.items()]
        node_option_strs = ['node[{0}="{1}"]'.format(k, v) for k, v in node_option_tuples]

        return 'graph G {\n' + \
            '\n'.join(graph_option_strs) + '\n' + \
            '\n'.join(node_option_strs) + '\n' + \
            content + '\n' + \
        '}'

class Node:
    def __init__(self, name):
        self.name = name
        self.links = set()
        self.options = {}

    def __str__(self):
        return '{0} ({1})'.format(self.name, len(self.links))

    def __hash__(self):
        return hash(self.name)

    def link(self, node):
        self.links.add(node)

    def graphviz(self):
        def links_generator():
            option_tuples = [(k, v) for k, v in self.options.items()]
            option_strs = ['{0}="{1}"'.format(k, v) for k, v in option_tuples]

            yield '{0} [{1}]'.format(self.name, ','.join(option_strs))

            for linked_node in self.links:

                if 'fillcolor' in self.options and 'fillcolor' in linked_node.options:
                    color_a_hsv = rgb_to_hsv(self.options['fillcolor'])
                    color_b_hsv = rgb_to_hsv(linked_node.options['fillcolor'])

                    average_color_hsv = tuple((a+b)/2 for a, b in zip(color_a_hsv, color_b_hsv))

                    average_color_rgb = hsv_to_rgb(average_color_hsv)


                    edge_options = 'color = "{}"'.format(average_color_rgb)

                yield '{0} -- {1} [{2}]'.format(self.name, linked_node.name, edge_options)

        return '\n'.join(list(links_generator()))

def cfg(name, suboptions=None):
    def parse_config_file(fname):
        """Parses the configuration file `fname`.

        `fname` must be a YAML file.

        Returns a configuration dictionary.
        """

        with codecs.open(fname, encoding='utf-8') as yaml_file:
            return yaml.load(yaml_file)

    def eval_option(option):
        if hasattr(option, '__call__'):
            return option()
        return option

    if suboptions == None:
        suboptions = CONFIG

    path = name.split('.')
    for part in path:
        if isinstance(suboptions, dict):
            if part in suboptions:
                suboptions = suboptions[part]
            else:
                return None
        elif isinstance(suboptions, (list, tuple)):
            index = int(part)
            return suboptions[index]
        else:
            return None

    return eval_option(suboptions)

def random_different_element(seq, not_this):
    assert len(seq) > 1
    while True:
        trial = random.choice(seq)
        if trial != not_this:
            return trial

def make_intragroup_links(nodes):
    for node in nodes:
        number_of_links = int(cfg('group.intralinks_per_node'))
        for i in range(number_of_links):
            linked_node = random_different_element(group, node)
            node.link(linked_node)

def make_intergroup_links(groups):
    for group in groups:
        for i in range(cfg('group.nodes_with_extralinks')):
            node = random.choice(group)
            number_of_links = int(cfg('group.extralinks_per_node'))
            for i in range(number_of_links):
                other_group = random_different_element(groups, group)
                linked_node = random.choice(other_group)
                node.link(linked_node)

def paint_node(node, basecolor):
    """
    Argumentos:

    - color: tuple em formato HSV: `(hue, saturation, value)`
    """

    fillcolor = basecolor.copy()
    bordercolor = hsv_change_brightness(fillcolor, -100)

    fillcolor_rgb = hsv_to_rgb(fillcolor)
    bordercolor_rgb = hsv_to_rgb(bordercolor)

    node.options['color'] = '{0}'.format(bordercolor_rgb)
    node.options['fillcolor'] = '{0}'.format(fillcolor_rgb)

if __name__ == '__main__':
    groups = []
    for i, group_options in enumerate(cfg('groups')):
        nodes = []
        for n in range(cfg('group.number_of_nodes')):
            name = 'g{0}_n{1}'.format(i, n)
            node = Node(name)
            node.options['label'] = ''

            basecolor_rgb = cfg('basecolor', group_options)
            brightness_offset = cfg('brightness_offset', group_options)

            basecolor_hsv = rgb_to_hsv(basecolor_rgb)

            changed_basecolor_hsv = hsv_change_brightness(basecolor_hsv, brightness_offset)

            paint_node(node, changed_basecolor_hsv)




            nodes.append(node)

        groups.append(nodes),

    for group in groups:
        make_intragroup_links(group)

    make_intergroup_links(groups)

    graph = Graph()
    graph.graph_options.update(cfg('graphviz.graph'))
    graph.node_options.update(cfg('graphviz.node'))

    for group in groups:
        for node in group:
            graph.nodes.add(node)

    print(graph.graphviz())
