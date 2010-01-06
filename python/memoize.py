"""\
Provides memoize function decorators.

Be cautions about using memoize to decorate a method (member function).
When applied to __call__ and __getitem__, at least, memoize
effectively transforms the function into a staticmethod.
"""

class memoize(object):
    def __init__(self, function, memos = None):
        if memos is None: memos = {}
        self.function = function
        self.memos = memos
    def flush(self):
        self.memos = type(self.memos)()
    def __call__(self, *arguments):
        if arguments not in self.memos:
            self.memos[arguments] = self.function(*arguments)
        return self.memos[arguments]

def custom_memoize(memos):
    def decorator(function):
        return memoize(function, memos)

if __name__ == '__main__':
    
    @memoize
    def factorial(n):
        if n > 0:
            return factorial(n - 1) * n
        else:
            return 1

    for n in range(50):
        print factorial(n)

    for n in range(50):
        factorial.flush()
        print factorial(n)

