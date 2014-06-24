# -*- encoding: utf-8 -*-

import sys
import os
import random
from subprocess import Popen, PIPE

from settings import LOGFILE, DEFAULT_EDGE_COLOR, BORDER_VALUE_OFFSET, GRAPHVIZ_OPTIONS
from colors import rgb_to_hsv, hsv_to_rgb, hsv_change_brightness, rgb_average

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
        >>> e1, e2, e3 = Edge(n1, n2), Edge(n1, n3), Edge(n2, n3)
        >>> g = Graph()
        >>> g.nodes = set([n1, n2, n3])
        >>> g.edges = set([e1, e2, e3])


    Then, you can output a Graphviz representation:

        >>> g.graphviz()
        graph G {
        n1 [fillcolor="#ffffff"]
        n2 [fillcolor="#ffffff"]
        n3 [fillcolor="#ffffff"]
        n1 -- n3 []
        n1 -- n2 []
        n2 -- n3 []
        }

    And save a PNG file rendered by Graphviz `fdp`:

        >>> g.save_png('my_graph.png')
    """

    def __init__(self):
        self.nodes = set()
        self.edges = set()
        self.graph_options = {}
        self.node_options = {}
        self.edge_options = {}

    def save_png(self, filename):
        """
        Renders this graph through `fdp` and saves the result in a PNG file.

        Arguments:
            - filename: a relative or absolute filename
        """
        debug("Salvando como PNG em '{0}'...".format(filename))
        if os.path.isfile(filename):
            os.unlink(filename)
        command = ["fdp", "-T", "png", "-o", filename]

        process = Popen(command, stdin=PIPE)
        process.communicate(input=self.graphviz())


    def graphviz(self):
        """
        Returns a string representing the graph, formatted as a Graphviz file.
        """
        content = '\n'.join(node.graphviz() for node in self.nodes) + '\n' + \
                  '\n'.join(edge.graphviz() for edge in self.edges)

        graph_option_tuples = [(k, v) for k, v in self.graph_options.items()]
        graph_option_strs = ['{0}="{1}"'.format(k, v) for k, v in graph_option_tuples]

        node_option_tuples = [(k, v) for k, v in self.node_options.items()]
        node_option_strs = ['node[{0}="{1}"]'.format(k, v) for k, v in node_option_tuples]

        edge_option_tuples = [(k, v) for k, v in self.edge_options.items()]
        edge_option_strs = ['edge[{0}="{1}"]'.format(k, v) for k, v in edge_option_tuples]

        return 'graph G {' + \
            '\n'.join(graph_option_strs) + '\n' + \
            '\n'.join(node_option_strs) + '\n' + \
            '\n'.join(edge_option_strs) + \
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
        """
        Returns a string representing the graph, formatted as a Graphviz file.
        """
        option_tuples = [(k, v) for k, v in self.options.items()]
        option_str = ','.join(['{0}="{1}"'.format(k, v) for k, v in option_tuples])

        return '{0} [{1}]'.format(self.name, option_str)


class Edge:
    def __init__(self, n1, n2):
        self._n1 = n1
        self._n2 = n2
        self.options = {}

    def graphviz(self):
        """
        Returns a string representing the graph, formatted as a Graphviz file.
        """
        option_tuples = [(k, v) for k, v in self.options.items()]
        option_str = ','.join(['{0}="{1}"'.format(k, v) for k, v in option_tuples])

        return '{0} -- {1} [{2}]'.format(self._n1.name, self._n2.name, option_str)


def cfg(name, config):
    """
    Accesses the `name` configuration inside `config`.

    The configuration data structure must be a `dict` containing any
    number of any nested structure of `list`s, `dict`s and values.

    The config name to be accessed must be a path connected by dots, like:

        groups.0.base_color

    The function descends through `config`, trying ot use each component
    first as a `dict` key, then as a `list` index, and if both fail,
    returns `None`.

    A proper configuration would then, for the config name above, access:

        config['groups'][0]['base_color']

    Which we could call the `VALUE`.

    The function then tries to call `VALUE` as a function. If this works, it
    returns the function value. If it fails, it returns `VALUE` itself.

    This is made this way so returned values are not restricted to
    deterministic values -- they may be functions returning random
    values, or values from a statistic distribution.

    Arguments:
        - name: a string representing a dot-separated path
        - config: a `dict` in the format explained above.
    """

    def filter_callable(option):
        """
        Returns the return value of `option` if it's a callable,
        and `option` itself otherwise.
        """
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

    return filter_callable(config)

def choose_another(seq, rejected):
    """
    Chooses randomically a value from seq which is not `rejected`.

    Arguments:
        - seq: a sequence
        - rejected: a value from `seq`
    """
    if len(seq) == 0:
        return None
    elif len(seq) == 1:
        return seq[0]
    else:
        while True:
            trial = random.choice(seq)
            if trial != rejected:
                return trial

def edge_color(n1, n2, config):
    """
    Returns the color of the edge between two nodes.

    The color is defined in the 'edge.color' configuration, if it
    exists, and on `settings.DEFAULT_EDGE_COLOR` otherwise.

    If 'edge.color' is the special string 'average', the returned color
    will be the average 'fillcolor' of the two nodes.

    Otherwise, it returns the RGB color defined.

    Arguments:
        - n1: a `Node` instance
        - n2: a `Node` instance
        - config: the configuration `dict` (see `cfg`)
    """
    color = cfg('edge.color', config) or DEFAULT_EDGE_COLOR
    if color == 'average':
        color = rgb_average(n1.options['fillcolor'], n2.options['fillcolor'])
    return color

def make_intragroup_links(group, graph, config):
    """
    Makes random links between nodes of a same group.

    Arguments:
        - group: a `dict` containing two keys:
            - 'nodes': a list of Node instances pertaining to this group
            - 'config': a configuration `dict` relative to this group (a
              part of the `config` argument)
        - graph: a `Graph` instance representing the whole graph
        - config: the configuration `dict` (see `cfg`)
    """
    nodes, group_config = group['nodes'], group['config']
    for node in nodes:
        number_of_links = int(cfg('intralinks_per_node', group_config))
        for i in range(number_of_links):
            linked_node = choose_another(nodes, node)
            edge = Edge(node, linked_node)
            edge.options['color'] = edge_color(node, linked_node, config)
            graph.edges.add(edge)

def make_intergroup_links(groups, graph, config):
    """
    Makes random links between nodes of different groups.

    Arguments:
        - groups: a `list` of `dict`s, each containing two keys:
            - 'nodes': a list of Node instances pertaining to this group
            - 'config': a configuration `dict` relative to this group (a
              part of the `config` argument)
        - graph: a `Graph` instance representing the whole graph
        - config: the configuration `dict` (see `cfg`)
    """
    for group in groups:
        for i in range(cfg('nodes_with_extralinks', group['config'])):
            node = random.choice(group['nodes'])
            number_of_links = int(cfg('extralinks_per_node', group['config']))
            for i in range(number_of_links):
                other_group = choose_another(groups, group)
                linked_node = random.choice(other_group['nodes'])
                edge = Edge(node, linked_node)
                edge.options['color'] = edge_color(node, linked_node, config)
                graph.edges.add(edge)

def make_node(name, group_options, config):
    """
    Builds a `Node` instance based on group and general configurations.

    Arguments:
        - name: a string containing the name of the node
        - group_options: a configuration `dict` relative to this group
          (a part of the `config` argument)
        - config: the configuration `dict` (see `cfg`)
    """

    def paint_node(node, basecolor_hsv):
        """
        Paints the node's fill and border colors.

        The base color passed is used directly in the fill color, and
        darkened to the border color.

        Arguments:

        - node: a `Node` instance; the node to be painted
        - basecolor_hsv: a HSV color (see module documentation)
        """

        fillcolor_hsv = basecolor_hsv[::]
        bordercolor_hsv = hsv_change_brightness(fillcolor_hsv, BORDER_VALUE_OFFSET)

        fillcolor_rgb = hsv_to_rgb(fillcolor_hsv)
        bordercolor_rgb = hsv_to_rgb(bordercolor_hsv)

        node.options['color'] = '{0}'.format(bordercolor_rgb)
        node.options['fillcolor'] = '{0}'.format(fillcolor_rgb)

    node = Node(name)
    node.options['label'] = ''

    basecolor_rgb = cfg('basecolor', group_options)
    value_offset = cfg('brightness_offset', group_options)

    basecolor_hsv = rgb_to_hsv(basecolor_rgb)

    changed_basecolor_hsv = hsv_change_brightness(basecolor_hsv, value_offset)

    paint_node(node, changed_basecolor_hsv)

    # As `node_diameter` may get below 0 for certain random
    # distributions, we have to keep generating him until it is positive
    node_diameter = -1
    while node_diameter < 0:
        node_diameter = cfg('node_diameter', group_options)

    node.options['width'] = node_diameter
    node.options['height'] = node_diameter

    return node

def make_graph(config):
    """
    Builds a `Graph` instance based on a graph configuration.

    Arguments:
        - config: the configuration `dict` (see `cfg`)
    """
    graph = Graph()
    graph.graph_options.update(cfg('graph', GRAPHVIZ_OPTIONS))
    graph.node_options.update(cfg('node', GRAPHVIZ_OPTIONS))
    graph.edge_options.update(cfg('edge', GRAPHVIZ_OPTIONS))

    groups = []

    for g, group_options in enumerate(cfg('groups', config)):

        nodes = []
        number_of_nodes = cfg('number_of_nodes', group_options)
        for n in range(number_of_nodes):
            name = 'g{0}_n{1}'.format(g, n)
            node = make_node(name, group_options, config)

            graph.nodes.add(node)
            nodes.append(node)

        groups.append({'nodes': nodes, 'config': group_options}),

    for group in groups:
        make_intragroup_links(group, graph, config)

    make_intergroup_links(groups, graph, config)


    return graph
