
from weakref import WeakKeyDictionary

class Kit(object):

    def __init__(self, kit = None, **keywords):

        self.__interfaces = WeakKeyDictionary()

        # copy the base kit
        if kit is not None:
            for key, value in vars(kit).items():
                setattr(self, key, value)

        # construct tools based on keywords
        for key, value in keywords.items():
            setattr(self, key, value)

    def get(self, interface, default = None):
        if interface not in self.__interfaces:
            if default is None:
                default = type(self)(kit = self)
            self.__interfaces[interface] = default
        return self.__interfaces[interface]

    __getitem__ = get

if __name__ == '__main__':

    class Joe(object):
        pass

    j = Joe()

    k = Kit()
    i = k.get(j)
    i.a = 10
    print i._Kit__interfaces.keys()
    print i.a

    del j
    print i._Kit__interfaces.keys()

