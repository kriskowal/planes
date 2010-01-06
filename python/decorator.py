
__all__ = (
    'wrap',
    'after_super',
    'before_super',
    'iter_after_super',
    'iter_before_super',
)

def wrap(wrapper):
    def wrap_this_function(function):
        def wrapped_function(*arguments, **keywords):
            return wrapper(function(*arguments, **keywords))
        return wrapped_function
    return wrap_this_function

if __name__ == '__main__':

    @wrap(list)
    def foo():
        yield "a"
    print foo()

def memoize(function):
    memos = {}
    def decorated(*arguments):
        if arguments not in memos:
            memos[arguments] = function(*arguments)
        return memos[arguments]
    return decorated

if __name__ == '__main__':
    
    @memoize
    def factorial(n):
        if n > 0:
            return factorial(n - 1) * n
        else:
            return 1

    for n in range(50):
        print factorial(n)

def _do_super(self, function_name, arguments, keywords):
    for klass in self.__class__.__mro__[1:]:
        if hasattr(klass, function_name):
            return getattr(klass, function_name)(self, *arguments, **keywords)

def after_super(function):
    function_name = function.func_name
    def wrapped(self, *arguments, **keywords):
        _do_super(self, function_name, arguments, keywords)
        return function(self, *arguments, **keywords)
    return wrapped

def before_super(function):
    function_name = function.func_name
    def wrapped(self, *arguments, **keywords):
        result = function(self, *arguments, **keywords)
        _do_super(self, function_name, arguments, keywords)
        return result
    return wrapped

if __name__ == '__main__':

    class Foo(object):
        def hi(self):
            print "Foo"

    class Bar(Foo):
        @before_super
        def hi(self):
            print "Bar"

    class Baz(Foo):
        @after_super
        def hi(self):
            print "Baz"

    bar = Bar()
    bar.hi()

    baz = Baz()
    baz.hi()

