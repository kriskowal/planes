
# 2004-08-07 refactored as indent_shift_iter.py
# 2004-05-30 created as indent.py, Kris Kowal

from tab_length import tab_length
from shift import shift

def shift_iter(
    source,
    initial = 0,
    start = 0,
    tab_length = tab_length,
    depth = None,
):
    """
    yields a sequence of all the lines from a given |source| that are one
     |tab_length| beneath their the |initial| column plus |start|, removing
     exactly enough white space to shift each line |tab_length| spaces
     left.
    """
    try:

        while True:

            # peek at the next line in the source iteration
            # if the source iteration has reached its end, this will raise
            #  a StopIteration
            # attempt to shift that line one tab width left
            line = shift(source.peek(), initial, start, tab_length, depth)

            # if there is not enough white space on the line to shift off
            if line == None:
                raise StopIteration
            else:
                # since we already peeked at the source line, discard it
                source.next()
                yield line

    except StopIteration:
        pass

if __name__ == '__main__':

    from planes.python.peekable import peekable
    def before_after(string, start = 0):
        source = peekable(iter(string.split("\n")))
        before = 0
        after = 0
        for line in shift_iter(source, start): before += 1
        for line in source: after += 1
        return (before, after)

    assert before_after("") == (1, 0)
    assert before_after("\ta\nb") == (1, 1)
    assert before_after("    a\nb") == (1, 1)
    assert before_after("a\nb") == (0, 2)

    assert before_after("        a") == (1, 0)
    assert before_after("       a") == (1, 0)
    assert before_after("      a") == (1, 0)
    assert before_after("     a") == (1, 0)
    assert before_after("    a") == (1, 0)
    assert before_after("   a") == (0, 1)
    assert before_after("  a") == (0, 1)
    assert before_after(" a") == (0, 1)
    assert before_after("a") == (0, 1)

    # for demonstration
    if False:

        data = """\
        a
    b

\tc
   \tc
b
c
        """
        print data.expandtabs(4)
        source = iter(data.split("\n"))
        print "Before:"
        for line in shift_iter(source):
            print line
        print "After:"
        for line in source:
            print line

