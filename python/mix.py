"""Provides a mix function for creating arbitrary multiple
inheritance subclasses at run time."""

def mix(*klasses):
    """returns a type that inherits from multiple superclasses.
    Accepts any number of class objects as arguments."""

    return type(
        "".join(
            klass.__name__
            for klass in klasses
        ),
        klasses,
        {}
    )

if __name__ == '__main__':

    class Foo(object):
        def a(self):
            return 'FooA!'
        def b(self):
            return 'FooB!'

    class Bar(object):
        def a(self):
            return 'BarA!'
        def b(self):
            return 'BarB!'

    FooBar = mix(Foo, Bar)
    foobar = FooBar()
    print foobar.a(), foobar.b()
    print foobar.__class__ == FooBar
    print foobar.__class__.__name__ == FooBar.__name__

