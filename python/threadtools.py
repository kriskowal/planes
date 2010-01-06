
__all__ = ['synchronized', 'ThreadedPromptController']

from threading import Semaphore, Lock
from threading import currentThread
import sys

def synchronized_method(function):
    """
    Java style synchronized. Use this on class methods. Adds a lock attribute
    called 'synch_lock' to each class instance that calls a synchronized
    method.
    """
    def wrapped(*arguments, **keywords):
        self = arguments[0]
        if not hasattr(self, 'synch_lock'):
            setattr(self, 'synch_lock', Lock())
        self.synch_lock.acquire()
        try:
            result = function(*arguments, **keywords)
            return result
        finally:
            self.synch_lock.release()
    return wrapped    
    

def synchronized_function(function, count = 1, semaphore = None):
    """Decorates a function with a semaphore so that only one thread may run 
    it at any time."""
    if semaphore is None:
        semaphore = Semaphore(count)
    def wrapped(*arguments, **keywords):
        semaphore.acquire()
        try:
            result = function(*arguments, **keywords)
            return result
        finally:
            semaphore.release()
    return wrapped

def Synchronized(*arguments, **keywords):
    return lambda function: synchronized(function, *arguments, **keywords)

def synchronized_property(attr, semaphore = None):
    if semaphore is None:
        semaphore = Semaphore(1)
    @Synchronized(semaphore = semaphore)
    def get(self):
        return getattr(self, attr)
    @Synchronized(semaphore = semaphore)
    def set(self, value):
        setattr(self, attr, value)
    return property(get, set)

# todo: implement rs = simultaneous(*fs)

class ThreadedPromptController:
    """
    Gives control over the prompt in a threaded environment.
    """

    def __init__(self, threadnames = True):
        self.threadnames = threadnames
        self.stdout = sys.stdout
        sys.stdout  = self
        self.prompt = '> '
        self.my_thread = currentThread()
        self.prompt_just_printed = False
    
    @synchronized_method
    def write(self, str):

        if str == ' ' or str == '\n': return
    
        if self.threadnames:
            name = '['+ currentThread().getName() + '] '
        else:
            name = ''
            
        if self.prompt_just_printed:
            self.stdout.write('\n')
            self.prompt_just_printed = False
            
        if len(str) > 0:
            self.stdout.write(name + str + '\n')
            #if not self.prompt_just_printed:
            #    self.print_prompt()
        
        if str == '' and currentThread() == self.my_thread:
            self.print_prompt() #self.stdout.write(name + self.prompt)
            self.prompt_just_printed = True

        self.stdout.flush()

    def close(self):
        sys.stdout = self.stdout
    
    def print_prompt(self):
        self.stdout.write(self.prompt)
        self.prompt_just_printed = True
         
    def __del__(self):
        self.close()
        
if __name__ == '__main__':

    class Foo(object):
        semaphore = Semaphore()
        a = synchronized_property('_a', semaphore)
        b = synchronized_property('_b', semaphore)

    foo = Foo()
    foo.a = 10
    print foo.a
    foo.b = 20
    print foo.b
        
