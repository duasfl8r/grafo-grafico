import random

class Graph:
    def __init__(self, groups):
        self.groups = groups

    def graphviz(self):
        content = "\n".join(group.graphviz() for group in self.groups)
        options = {
                "overlap": "false",
                "outputorder": "edgesfirst"
        }

        node_options = {
                "style": "filled"
        }

        options_str = "\n".join('{0}={1}'.format(k, v) for k, v in options.items())
        node_options_content_str = ",".join('{0}={1}'.format(k, v) for k, v in node_
        node_options_str = "node[{0}]".format(node_options_content_str)
        return "graph G {\n" + "\n" + node_options_str + "\n" + options_str + "\n" +

class Node:
    def __init__(self, name):
        self.name = name
        self.links = set()

    def __str__(self):
        return "{0} ({1})".format(self.name, len(self.links))

    def __hash__(self):
        return hash(self.name)

    def link(self, node):
        self.links.add(node)

    def graphviz(self):
        def links_generator():
            for linked_node in self.links:
                yield "{0} -- {1}".format(self.name, linked_node.name)

        return "\n".join(list(links_generator()))

class Group:
    def __init__(self, nodes):
        self.nodes = nodes

    def __str__(self):
        return "<Group: {0}>".format(", ".join(str(n) for n in self.nodes))

    def graphviz(self):
        return "\n".join(node.graphviz() for node in self.nodes)

if __name__ == '__main__':
    nodes = {
        "1": Node("1"),
        "2": Node("2"),
        "3": Node("3"),
        "4": Node("4"),
    }

    nodes = []
    for n in range(100):
        nodes.append(Node(str(n)))

    def random_different_node(nodes, not_this):
        assert len(nodes) > 1
        while True:
            trial = random.choice(nodes)
            if trial != not_this:
                return trial

    for node in nodes:
        number_of_links = round(random.gauss(5, 3))
        for i in range(number_of_links):
            linked_node = random_different_node(nodes, node)
            node.link(linked_node)

    graph = Graph(groups=[
            Group(nodes),
        ]
    )

    print(graph.graphviz())
