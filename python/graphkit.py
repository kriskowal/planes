
from os import popen3
from cStringIO import StringIO
from planes.python.xml.tags import tags as xml_tags, Tag

class Edge(object):
    def __init__(self, node, name = None):
        self.node = node
        self.name = name

class Node(object):

    def __init__(self, name, edges = None):
        self.name = name
        if edges is None: edges = set()
        self.edges = edges

    def connect(self, node, name = None):
        self.edges.add(Edge(node, name))

    def __str__(self):
        return "%s%s" % (
            "node %s;\n" % self.name,
            "".join( # edges
                edge.name and
                "edge[label=%s] %s -> %s;\n" % (edge.name, self.name, edge.node.name) or
                "%s -> %s;\n" % (self.name, edge.node.name)
                for edge in self.edges
            )
        )

class Graph(object):

    def __init__(self, nodes = None, name = None):
        if name is None: name = 'Graph'
        if nodes is None:
            nodes = set()
        self.name = name
        self.nodes = nodes

    def __str__(self):
        return digraph_str(
            (node.name, edge.node.name)
            for node in self.nodes
            for edge in node.edges
        )

    def connect(self, source, target, name = None):
        source.connect(target, name)

    def file(self, type = 'png'):
        from os import popen3
        stdin, stdout, stderr = popen3(['dot', '-T' + type])
        stdin.write(str(self))
        stdin.close()
        stderr.close()
        return stdout

    def __html_repr__(self, kit):

        tags = kit.tags
        if tags is None: tags = xml_tags

        type = 'gif'

        from os import popen3
        stdin, stdout, stderr = popen3(['dot', '-T' + type])
        stdin.write(str(self))
        stdin.close()

        error = stderr.read()
        print error

        return tags.img(
            src = kit.host(
                file = stdout,
                content_type = 'image/' + type
            ),
            alt = self.name,
            onload = 'messageBuffer.autoScroll()',
        )

class dot_gif(str):
    def __html_repr__(self, kit):

        tags = kit.tags
        if tags is None: tags = xml_tags

        stdin, stdout, stderr = popen3(['dot','-Tgif'])

        stdin.write(self)
        stdin.close()

        return tags.img(
            src = host(
                stdout,
                content_type = 'image/gif'
            ),
            onload = 'messageBuffer.autoScroll()',
        )

class dot_svg(str):
    def __html_repr__(self, kit):

        tags = kit.tags
        if tags is None: tags = xml_tags

        stdin, stdout, stderr = popen3(['dot','-Tsvg'])

        stdin.write(self)
        stdin.close()

        error = stderr.read().strip()
        if error: print error
        stderr.close()

        svg = stdout.read()
        result_xml = Tag.parseString(svg)
        height = result_xml['height']
        width = result_xml['width']

        stdout = StringIO(svg)

        return tags.object(
            type = 'image/svg+xml',
            data = host(
                stdout,
                content_type = 'image/svg+xml'
            ),
            onload = 'messageBuffer.autoScroll()',
            style = 'width: %s; height: %s' % (width, height),
        )

dot = dot_gif

def graph_str(edges):
    return "graph {\n%s}\n" % "".join(
        "%s -- %s;\n" % edge
        for edge in edges
    )

def digraph_str(edges):
    return "digraph {\n%s}\n" % "".join(
        "%s -> %s;\n" % edge
        for edge in edges
    )

def digraph(edges, name = None):

    edges = list(edges)
    sources = list(edge[0] for edge in edges)
    targets = list(edge[1] for edge in edges)
    nodes = dict((name, Node(name)) for name in set(sources + targets))
    graph = Graph(nodes.values(), name) 

    for edge in edges:
        source, target = (nodes[name] for name in edge[0:2])
        if len(edge) == 3:
            graph.connect(source, target, edge[2])
        elif len(edge) == 2:
            graph.connect(source, target)
        else:
            raise ValueError("Two labels needed to create an edge")

    return graph

