import sys
import random
import colorsys

try:
    from config import CONFIG
except ImportError:
    sys.stderr.write('Arquivo `config.py` não encontrado. Você já o copiou de `config-dist.py?`')
    sys.exit(-1)


from colors import rgb_hex_to_rgb_dec, rgb_dec_to_rgb_hex, hsv_change_brightness

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

                if self.options['fillcolor'] and linked_node.options['fillcolor']:
                    color_a_rgb_dec = rgb_hex_to_rgb_dec(self.options['fillcolor'])
                    color_b_rgb_dec = rgb_hex_to_rgb_dec(linked_node.options['fillcolor'])
                    color_a_hsv = colorsys.rgb_to_hsv(*color_a_rgb_dec)
                    color_b_hsv = colorsys.rgb_to_hsv(*color_b_rgb_dec)

                    average_color_hsv = tuple((a+b)/2 for a, b in zip(color_a_hsv, color_b_hsv))
                    average_color_rgb_dec = [int(v) for v in colorsys.hsv_to_rgb(*average_color_hsv)]

                    average_color_rgb_hex = rgb_dec_to_rgb_hex(average_color_rgb_dec)


                    edge_options = 'color = "{}"'.format(average_color_rgb_hex)

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
        number_of_links = cfg('group.intralinks_per_node')
        for i in range(number_of_links):
            linked_node = random_different_element(group, node)
            node.link(linked_node)

def make_intergroup_links(groups):
    for group in groups:
        for i in range(cfg('group.nodes_with_extralinks')):
            node = random.choice(group)
            number_of_links = cfg('group.extralinks_per_node')
            for i in range(number_of_links):
                other_group = random_different_element(groups, group)
                linked_node = random.choice(other_group)
                node.link(linked_node)

if __name__ == '__main__':
    groups = []
    for i, group_options in enumerate(cfg('groups')):
        nodes = []
        for n in range(cfg('group.number_of_nodes')):
            name = 'g{0}_n{1}'.format(i, n)
            node = Node(name)
            node.options['label'] = ''

            basecolor_rgb_dec = cfg('basecolor', group_options)

            fillcolor_hsv = list(colorsys.rgb_to_hsv(*basecolor_rgb_dec))
            brightness_offset = cfg('brightness_offset', group_options)

            fillcolor_hsv = hsv_change_brightness(fillcolor_hsv, brightness_offset)
            color_hsv = hsv_change_brightness(fillcolor_hsv, -100)

            fillcolor_rgb_dec = [int(v) for v in colorsys.hsv_to_rgb(*fillcolor_hsv)]
            color_rgb_dec = [int(v) for v in colorsys.hsv_to_rgb(*color_hsv)]

            fillcolor_rgb = rgb_dec_to_rgb_hex(fillcolor_rgb_dec)
            color_rgb = rgb_dec_to_rgb_hex(color_rgb_dec)

            node.options['color'] = '{0}'.format(color_rgb)
            node.options['fillcolor'] = '{0}'.format(fillcolor_rgb)

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
