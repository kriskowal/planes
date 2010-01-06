
class peekable(object):
    """
        a peekable iteration.  Wraps a source iteration transparently and
         allows the user to "peek" at the next element without eating it.
         Effectively, the peeked element _is_ eaten from the source iteration,
         so it is imperative that the peek have exclusive access to the
         iteration.  This entails ditching all references to the source
         iteration and using the peekable as its sole accessor.
    """

    # I considered having this class assert the axiom that the reference
    #  count on source is exactly 1 (actually 2, counting the reference
    #  used in the refcount function call), but decided against it on grounds
    #  of unforeseeable uses of the source iteration.  For example, it
    #  might be a "pipe" iteration, whereby elements are inserted in
    #  FIFO fashion and yielded as available.  This behavior would require
    #  that others have references to the source.

    def __init__(self, source):
        self.peeked = []
        self.source = source

    def peek(self):
        """
            |peek| behaves exactly the same way as |next| except has no
            side effects.  That is, calls of |peek| will always return the
            same element until |next| is called.
        """
        if not len(self.peeked):
            self.peeked.append(self.source.next())
        return self.peeked[0]

    def peek_iter(self):
        """
            |peek_iter| behaves exactly the same way as |iter| except has
            no side effects.  That is, calls of |peek_iter| will always
            iterate on the same elements of the source iteration until
            |next| is called, consuming the first element of the |source|.
        """
        for element in self.peeked:
            yield element
        for element in self.source:
            self.peeked.append(element)
            yield element

    def __iter__(self):
        return self

    def next(self):
        """
            returns the next, unconsumed, element of the |source| iteration.
        """
        if len(self.peeked):
            peeked = self.peeked[0]
            self.peeked = self.peeked[1:]
            return peeked
        else:
            return self.source.next()

