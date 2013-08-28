class Graph:
    def __init__(self, groups):
        self.groups = groups

    def graphviz(self):
        content = "\n".join(group.graphviz() for group in self.groups)
        return "graph G {\n" + content + "\n}"

class Node:
    def __init__(self, name):
        self.name = name
        self.links = set()

    def __hash__(self):
        return hash((self.name, tuple(self.links)))

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

    def graphviz(self):
        return "\n".join(node.graphviz() for node in self.nodes)

if __name__ == '__main__':
    nodes = {
        "1": Node("1"),
        "2": Node("2"),
        "3": Node("3"),
        "4": Node("4"),
    }

    nodes["1"].link(nodes["2"])
    nodes["1"].link(nodes["4"])
    nodes["2"].link(nodes["3"])
    nodes["4"].link(nodes["3"])

    graph = Graph(groups=[
            Group(nodes.values()),
        ]
    )

    print(graph.graphviz())
