#!/usr/bin/env python

from twisted.internet import reactor
from planes.python.iterkit import any

def asynchronous(reactor = reactor):
    def wrapped(function):
        def wrapped(*arguments, **keywords):
            generator = function(*arguments, **keywords)
            def next():
                try:
                    result = generator.next()
                    if any(
                        isinstance(result, klass)
                        for klass in (int, float)
                    ):
                        reactor.callLater(result, next)
                    else:
                        raise TypeError(
                            'anynchronous generators must yield ' + 
                            'seconds to wait as numeric ' +
                            'values.  got %s.' % 
                            `result.__class__.__name__`
                        )
                except StopIteration:
                    pass
            next()
        return wrapped
    return wrapped

if __name__ == '__main__':

    @asynchronous(reactor)
    def start_routine(name, start, step, stop):
        n = 0
        while start < stop:
            print 'routine %s step %s waiting %s' % (name, n, start)
            yield start
            start += step
            n += 1
        reactor.stop()

    start_routine('A', 0, 1, 5)
    start_routine('B', 2, 0.5, 5)
    #start_routine('C', 'Joe', 'Joe', 'Joe1')

    reactor.run()

