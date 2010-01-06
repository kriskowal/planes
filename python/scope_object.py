
class ScopeObject(object):

    def __init__(self, *parents):
        super(ScopeObject, self).__init__()
        self.__dict__['_ScopeObject__parents'] = parents

    def __getattr__(self, key):
        for parent in self.__parents:
            if hasattr(parent, key):
                return getattr(parent, key)
        return super(ScopeObject, self).__getattr__(key)

    def __setattr__(self, key, value):
        for parent in self.__parents:
            if hasattr(parent, key):
                return setattr(parent, key, value)
        return super(ScopeObject, self).__setattr__(key, value)

if __name__ == '__main__':

    foo = ScopeObject()
    foo.a = 10
    print hasattr(foo, 'a')
    print hasattr(foo, 'b')
    print foo.a

    bar = ScopeObject(foo)
    bar.b = 20
    print bar.a
    print bar.b
    print hasattr(bar, 'a')
    print hasattr(bar, 'b')
    print hasattr(bar, 'c')

