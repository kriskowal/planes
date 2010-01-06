
from planes.lazy import DhtService, PathService, StandardService, serve
from sys import argv
from random import choice

nodes = []
for n in range(20):
    node = DhtService('/%s' % n)
    if len(nodes):
        node.join(choice(nodes)[1])
    nodes.append([n, node])

nodes[0][1].data['hi'] = 'world'

serve(
    StandardService(
        PathService(paths = dict(
            ('%s' % n, node)
            for n, node in nodes
        ))
    ),
    port = int(argv[1]),
    debug = True
)

