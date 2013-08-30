import random
from settings import get_setting as S

class Graph:
    def __init__(self, groups):
        self.groups = groups

    def graphviz(self):
        content = '\n'.join(group.graphviz() for group in self.groups)
        options = {
                'overlap': 'false',
                'outputorder': 'edgesfirst'
        }

        node_options = {
                'style': 'filled',
                'regular': 'true',
        }

        options_str = '\n'.join('{0}={1}'.format(k, v) for k, v in options.items())
        node_options_content_str = ','.join('{0}={1}'.format(k, v) for k, v in node_options.items())
        node_options_str = 'node[{0}]'.format(node_options_content_str)
        return 'graph G {\n' + '\n' + node_options_str + '\n' + options_str + '\n' + content + '\n}'

class Node:
    def __init__(self, name):
        self.name = name
        self.links = set()

    def __str__(self):
        return '{0} ({1})'.format(self.name, len(self.links))

    def __hash__(self):
        return hash(self.name)

    def link(self, node):
        self.links.add(node)

    def graphviz(self):
        def links_generator():
            yield '{0} [label=""]'.format(self.name)
            for linked_node in self.links:
                yield '{0} -- {1}'.format(self.name, linked_node.name)

        return '\n'.join(list(links_generator()))

class Group:
    def __init__(self, nodes):
        self.nodes = nodes

    def __str__(self):
        return '<Group: {0}>'.format(', '.join(str(n) for n in self.nodes))

    def graphviz(self):
        return '\n'.join(node.graphviz() for node in self.nodes)

if __name__ == '__main__':

    def random_different_element(seq, not_this):
        assert len(seq) > 1
        while True:
            trial = random.choice(seq)
            if trial != not_this:
                return trial

    groups = []
    for g in range(S('graph.number_of_groups')):
        nodes = []
        for n in range(S('group.number_of_nodes')):
            name = 'n{0}x{1}'.format(g, n)
            nodes.append(Node(name))

        groups.append(Group(nodes)),

    # Ligações intra-grupos
    for group in groups:
        for node in group.nodes:
            number_of_links = S('group.intralinks_per_node')
            for i in range(number_of_links):
                linked_node = random_different_element(group.nodes, node)
                node.link(linked_node)

    for group in groups:
        for i in range(S('group.nodes_with_extralinks')):
            node = random.choice(group.nodes)
            number_of_links = S('group.extralinks_per_node')
            for i in range(number_of_links):
                other_group = random_different_element(groups, group)
                linked_node = random.choice(other_group.nodes)
                node.link(linked_node)

    graph = Graph(groups)

    print(graph.graphviz())
