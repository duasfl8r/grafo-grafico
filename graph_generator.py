# -*- encoding: utf-8 -*-

import sys
import os
import random
from subprocess import Popen, PIPE

from settings import LOGFILE
from colors import rgb_to_hsv, hsv_to_rgb, hsv_change_brightness, rgb_hex_to_decimal, rgb_decimal_to_hex, rgb_average

def debug(msg):
    with open(LOGFILE, 'a') as logfile:
        logfile.write(msg + '\n')

class Graph:
    def __init__(self):
        self.nodes = set()
        self.graph_options = {}
        self.node_options = {}

    def save_png(self, filename):
        debug("Salvando como PNG em '{0}'...".format(filename))
        command = ["fdp", "-T", "png", "-o", filename]

        process = Popen(command, stdin=PIPE)
        process.communicate(input=self.graphviz())


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
                edge_color = rgb_average(self.options['fillcolor'], linked_node.options['fillcolor'])
                edge_options = 'color = "{}"'.format(edge_color)

                yield '{0} -- {1} [{2}]'.format(self.name, linked_node.name, edge_options)

        return '\n'.join(list(links_generator()))

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

def make_intragroup_links(nodes, config):
    for node in nodes:
        number_of_links = int(cfg('group.intralinks_per_node', config))
        for i in range(number_of_links):
            linked_node = try_to_choose_another(nodes, node)
            node.link(linked_node)

def make_intergroup_links(groups, config):
    for group in groups:
        for i in range(cfg('group.nodes_with_extralinks', config)):
            node = random.choice(group)
            number_of_links = int(cfg('group.extralinks_per_node', config))
            for i in range(number_of_links):
                other_group = try_to_choose_another(groups, group)
                linked_node = random.choice(other_group)
                node.link(linked_node)

def make_node(name, group_index, config):
    group_options = cfg('groups.{}'.format(group_index), config)

    node = Node(name)
    node.options['label'] = ''

    basecolor_rgb = cfg('basecolor', group_options)
    brightness_offset = cfg('brightness_offset', group_options)

    basecolor_hsv = rgb_to_hsv(basecolor_rgb)

    changed_basecolor_hsv = hsv_change_brightness(basecolor_hsv, brightness_offset)

    paint_node(node, changed_basecolor_hsv)

    return node

def paint_node(node, basecolor):
    """
    Argumentos:

    - color: tuple em formato HSV: `(hue, saturation, value)`
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
        make_intragroup_links(group, config)

    make_intergroup_links(groups, config)


    return graph
