
from planes.lazy import PathService, FunctionService, GraphService, Service, Response
from planes.response import Page, Redirect, tags
from socket import gethostname
from planes.python.graphkit import *

class DhtService(PathService):

    def __init__(self, url = None):
        self.next = self
        self.prev = self
        self.data = {}
        self.url = url

        @FunctionService
        def get(kit, key):
            if key not in self.data:
                return Redirect('%s/get/%s' % (self.next.url, key))
            return Response(self.data[key])

        @FunctionService
        def set(kit, key, value):
            self.data[key] = value
            return Response(value)

        @FunctionService
        def delete(kit, key):
            del self.data[key]

        @FunctionService
        def has(kit, key):
            return key in self.data

        @GraphService
        def report(kit):
            return 'digraph {node [shape=record]; %s}' % ''.join([
                '"%s" [label="{%s|%s}"]; edge "%s" -> "%s"; ' % (
                    node.url,
                    node.url,
                    ", ".join([
                        "%s: %s" % items
                        for items in node.data.items()
                    ]),
                    node.url,
                    node.next.url,
                )
                for node in self.ring()
            ])

        self.paths = {
            'get': get,
            'set': set,
            'del': delete,
            'has': has,
            'report': report,
        }

        super(DhtService, self).__init__()

    def ring(self):
        node = self
        while True:
            yield node
            node = node.next
            if node is self:
                break

    def join(self, node):
        temp = self.next
        self.next = node
        node.prev.next = temp
        temp.prev = node.prev
        node.prev = self

