import random
import colorsys

from settings import get_setting as S

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

def random_different_element(seq, not_this):
    assert len(seq) > 1
    while True:
        trial = random.choice(seq)
        if trial != not_this:
            return trial

def make_intragroup_links(nodes):
    for node in nodes:
        number_of_links = S('group.intralinks_per_node')
        for i in range(number_of_links):
            linked_node = random_different_element(group, node)
            node.link(linked_node)

def make_intergroup_links(groups):
    for group in groups:
        for i in range(S('group.nodes_with_extralinks')):
            node = random.choice(group)
            number_of_links = S('group.extralinks_per_node')
            for i in range(number_of_links):
                other_group = random_different_element(groups, group)
                linked_node = random.choice(other_group)
                node.link(linked_node)

def hsv_color_variant(hsv_color, brightness_offset):
    new_hsv_color = list(hsv_color)

    new_hsv_color[2] += brightness_offset

    if new_hsv_color[2] < 0 or new_hsv_color[2] > 255:
        return hsv_color

    return new_hsv_color

def rgb_hex_to_rgb_dec(rgb_hex):
    assert(len(rgb_hex) == 7), rgb_hex

    hex_colors = [rgb_hex[i:i+2] for i in [1, 3, 5]]
    return tuple(int(c, 16) for c in hex_colors)

def rgb_dec_to_rgb_hex(rgb_dec):
    assert(len(rgb_dec) == 3)

    hex_colors = ['{:0>2}'.format(hex(v)[2:]) for v in rgb_dec]
    return '#' + ''.join(hex_colors)

if __name__ == '__main__':
    groups = []
    for i, group_settings in enumerate(S('groups')):
        nodes = []
        for n in range(S('group.number_of_nodes')):
            name = 'g{0}_n{1}'.format(i, n)
            node = Node(name)
            node.options['label'] = ''

            basecolor_rgb_dec = S('basecolor', group_settings)

            fillcolor_hsv = list(colorsys.rgb_to_hsv(*basecolor_rgb_dec))
            brightness_offset = S('brightness_offset', group_settings)

            fillcolor_hsv = hsv_color_variant(fillcolor_hsv, brightness_offset)
            fillcolor_rgb_dec = [int(v) for v in colorsys.hsv_to_rgb(*fillcolor_hsv)]

            fillcolor_rgb = rgb_dec_to_rgb_hex(fillcolor_rgb_dec)

            node.options['fillcolor'] = '{0}'.format(fillcolor_rgb)

            nodes.append(node)

        groups.append(nodes),

    for group in groups:
        make_intragroup_links(group)

    make_intergroup_links(groups)

    graph = Graph()
    graph.graph_options.update(S('graphviz.graph'))
    graph.node_options.update(S('graphviz.node'))

    for group in groups:
        for node in group:
            graph.nodes.add(node)

    print(graph.graphviz())
