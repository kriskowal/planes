
from planes.python.graphkit import digraph

def classgraph(klass):
    if not isinstance(klass, type):
        klass = klass.__class__
    if isinstance(klass, type):
        edges = []
        def classname(base):
            if base.__module__ == klass.__module__:
                return base.__name__
            else:
                return '"%s.%s"' % (
                    base.__module__,
                    base.__name__
                )
        for superclass in klass.__mro__:
            for baseclass in superclass.__bases__:
                edges.append((classname(superclass), classname(baseclass)))
        return digraph(edges)
    else:
        raise Exception('classgraph does not yet work for classobjs')

