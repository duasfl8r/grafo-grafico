# -*- encoding: utf-8 -*-

import sys
import os
import random
from subprocess import Popen, PIPE

from settings import LOGFILE
from colors import rgb_to_hsv, hsv_to_rgb, hsv_change_brightness, rgb_hex_to_decimal, rgb_decimal_to_hex, rgb_average

def debug(msg):
    """
    Debugs a message to a log file.
    """
    with open(LOGFILE, 'a') as logfile:
        logfile.write(msg + '\n')

class Graph:
    """
    Represents a graph, holding a set of nodes and Graphviz options.

    How to use this class
    ---------------------

    Create an instance and populate its nodes:

        >>> n1, n2, n3 = Node('n1'), Node('n2'), Node('n3')
        >>> n1.link(n2)
        >>> n1.link(n3)
        >>> n2.link(n3)
        >>> g = Graph()
        >>> g.nodes = set([n1, n2, n3])

    Then, you can output a Graphviz representation:

        >>> g.graphviz()
        graph G {
        n1 [fillcolor="#ffffff"]
        n1 -- n2 [color = "#000000"]
        n1 -- n3 [color = "#000000"]
        n2 [fillcolor="#ffffff"]
        n2 -- n3 [color = "#000000"]
        n3 [fillcolor="#ffffff"]
        }

    And save a PNG file rendered by Graphviz `fdp`:

        >>> g.save_png('my_graph.png')
    """

    def __init__(self):
        self.nodes = set()
        self.edges = set()
        self.graph_options = {}
        self.node_options = {}

    def save_png(self, filename):
        """
        Renders this graph through `fdp` and saves the result in a PNG file.

        Arguments:
            - filename: a relative or absolute filename
        """
        debug("Salvando como PNG em '{0}'...".format(filename))
        command = ["fdp", "-T", "png", "-o", filename]

        process = Popen(command, stdin=PIPE)
        process.communicate(input=self.graphviz())


    def graphviz(self):
        content = '\n'.join(node.graphviz() for node in self.nodes) + '\n' \
                  '\n'.join(edge.graphviz() for edge in self.edges)

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
        self.options = {'fillcolor': '#ffffff'}

    def __str__(self):
        return '<Node: {0}>'.format(self.name)

    def __hash__(self):
        return hash(self.name)

    def graphviz(self):
        option_tuples = [(k, v) for k, v in self.options.items()]
        option_str = '\n'.join(['{0}="{1}"'.format(k, v) for k, v in option_tuples])

        return '{0} [{1}]'.format(self.name, option_str)


class Edge:
    def __init__(self, n1, n2):
        self._n1 = n1
        self._n2 = n2
        self.options = {}

    def graphviz(self):
        option_tuples = [(k, v) for k, v in self.options.items()]
        option_str = '\n'.join(['{0}="{1}"'.format(k, v) for k, v in option_tuples])

        return '{0} -- {1} [{2}]'.format(self._n1.name, self._n2.name, option_str)


def cfg(name, config):
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

    path = name.split('.')
    for part in path:
        if isinstance(config, dict):
            if part in config:
                config = config[part]
            else:
                return None
        elif isinstance(config, (list, tuple)):
            index = int(part)
            return config[index]
        else:
            return None

    return eval_option(config)

def try_to_choose_another(seq, not_this):
    if len(seq) == 0:
        return None
    elif len(seq) == 1:
        return seq[0]
    else:
        while True:
            trial = random.choice(seq)
            if trial != not_this:
                return trial

def edge_color(n1, n2, config):
    color = cfg('edge.color', config) or '#000000'
    if color == 'average':
        color = rgb_average(n1.options['fillcolor'], n2.options['fillcolor'])
    return color

def make_intragroup_links(nodes, graph, config):
    for node in nodes:
        number_of_links = int(cfg('group.intralinks_per_node', config))
        for i in range(number_of_links):
            linked_node = try_to_choose_another(nodes, node)
            edge = Edge(node, linked_node)
            edge.options['color'] = edge_color(node, linked_node, config)
            graph.edges.add(edge)

def make_intergroup_links(groups, graph, config):
    for group in groups:
        for i in range(cfg('group.nodes_with_extralinks', config)):
            node = random.choice(group)
            number_of_links = int(cfg('group.extralinks_per_node', config))
            for i in range(number_of_links):
                other_group = try_to_choose_another(groups, group)
                linked_node = random.choice(other_group)
                edge = Edge(node, linked_node)
                edge.options['color'] = edge_color(node, linked_node, config)
                graph.edges.add(edge)

def make_node(name, group_index, config):
    group_options = cfg('groups.{}'.format(group_index), config)

    node = Node(name)
    node.options['label'] = ''

    basecolor_rgb = cfg('basecolor', group_options)
    brightness_offset = cfg('brightness_offset', group_options)

    basecolor_hsv = rgb_to_hsv(basecolor_rgb)

    changed_basecolor_hsv = hsv_change_brightness(basecolor_hsv, brightness_offset)

    paint_node(node, changed_basecolor_hsv)

    # As `node_diameter` may get below 0 for certain random
    # distributions, we have to keep generating him until it is positive
    node_diameter = -1
    while node_diameter < 0:
        node_diameter = cfg('node_diameter', group_options)

    node.options['width'] = node_diameter
    node.options['height'] = node_diameter

    return node

def paint_node(node, basecolor):
    """
    Args:

    - color: tuple HSV format: `(hue, saturation, value)`
    """

    fillcolor = basecolor[::]
    bordercolor = hsv_change_brightness(fillcolor, -0.4)

    fillcolor_rgb = hsv_to_rgb(fillcolor)
    bordercolor_rgb = hsv_to_rgb(bordercolor)

    node.options['color'] = '{0}'.format(bordercolor_rgb)
    node.options['fillcolor'] = '{0}'.format(fillcolor_rgb)

def make_graph(config):
    graph = Graph()
    graph.graph_options.update(cfg('graphviz.graph', config))
    graph.node_options.update(cfg('graphviz.node', config))

    groups = []

    for g, group_options in enumerate(cfg('groups', config)):
        number_of_nodes = cfg('group.number_of_nodes', config)

        nodes = []
        for n in range(number_of_nodes):
            name = 'g{0}_n{1}'.format(g, n)
            node = make_node(name, g, config)

            graph.nodes.add(node)
            nodes.append(node)

        groups.append(nodes),

    for group in groups:
        make_intragroup_links(group, graph, config)

    make_intergroup_links(groups, graph, config)


    return graph
