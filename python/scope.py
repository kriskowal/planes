
from wrap import wrap
from iterkit import any

# this is a utility 'higher-order' function that
#  generates Scope member functions: iterkeys,
#  itervalues, iteritems for Scope
def itermethod(attribute):
    def method(self):
        for iterand in getattr(super(Scope, self), attribute)():
            yield iterand
        for parent in self.parents:
            for iterand in getattr(parent, attribute)():
                yield iterand
    return method

class Scope(dict):

    def __init__(self, *parents):
        super(Scope, self).__init__()
        self.parents = parents

    def has_key(self, key):
        if super(Scope, self).__contains__(key):
            return True
        return any(
            key in parent.keys()
            for parent in self.parents
        )

    def get(self, key):
        if super(Scope, self).__contains__(key):
            return super(Scope, self).__getitem__(key)
        for parent in self.parents:
            if key in parent:
                return parent[key]
        # effectively, raise a dict exception if
        #  we fail to find the key in self or any parent
        return super(Scope, self).__getitem__(key)

    __contains__ = has_key
    __getitem__ = get
    iterkeys = itermethod('keys')
    itervalues = itermethod('values')
    iteritems = itermethod('items')
    keys = wrap(tuple)(iterkeys)
    values = wrap(tuple)(itervalues)
    items = wrap(tuple)(iteritems)

    def __repr__(self):
        return repr(dict(self.items()))

if __name__ == '__main__':
    a = {'a': 10}
    b = {'b': 20}
    c = Scope(a, b)
    c['c'] = 30
    print c['a']
    print c.items()
    print c.keys()
    print c.values()
    print 'a' in c
    print 'b' in c
    print 'c' in c
    print 'd' in c

    walls = {}
    characters = {}
    furniture = {}
    objects = Scope(
        walls,
        characters,
        furniture
    )
    walls['n'] = '-'
    walls['e'] = '|'
    characters['bob'] = "bob's character"
    print "Objects:"
    print objects
    print "objects['n']"
    print objects['n']
    print "objects['e']"
    print objects['e']
    print "objects['bob']"
    print objects['bob']
    print "objects.keys()"
    print objects.keys()
    print "objects.values()"
    print objects.values()
    print "dict(objects.items())"
    print dict(objects.items())

    print c['d'] # should raise an exception

