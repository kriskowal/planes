
from planes.python.xml.tags import tags
from threading import Semaphore

class pipe(object):
    length = 256
    def __init__(self, length = None):
        if length is not None: self.length = length
        self.semaphore = Semaphore(length)
        self.items = []
    def __next__(self):
        return self.items.shift()
        self.semaphore.release()
    def send(item):
        self.semaphore.acquire()
        self.items.append(item)
    def __html_repr__(self):
        pass

class async(object):
    def __init__(self, function, *arguments, **keywords):
        pass
    def __call__(self):
        # return a pipe
        return 
    def __html_repr__(self):
        pass

class pipeline(object):
    def __init__(self, *asyncs):
        pass
    def __call__(self):
        pass
    def __html_repr__(self):
        pass

