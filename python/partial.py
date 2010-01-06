
class Partial:
    """
    Allows the partial application of a function.

    >>> f = Partial(len, [1,2,3])
    >>> f()
    3

    >>> g = Partial(lambda x,y,z: x+y+z, 1)
    >>> g(1,1)
    3

    """
    def __init__(self, function, *args, **kws):
        self.function = function
        self.args = args
        self.kws = kws
    def __call__(self, *args, **kws):
        for key, value in kws.items():
            self.kws[key] = value
        return self.function(*(self.args+args), **(self.kws))

