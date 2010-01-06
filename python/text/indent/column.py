
# 2004-08-07 by Kris Kowal

from tab_length import tab_length
from next_tab import next_tab

def column(line, column = 0, tab_length = tab_length):
    """
        returns the |column| offset that the cursor would end on if this
         |line| were printed out on a perfect terminal, starting at |column|,
         assuming tab stops at equal intervals of |tab_length|, where
         |tab_length| is a power of two.
        A perfect terminal is one which has no horizontal nor vertical size
         constraints.
    """

    # todo: consider: assumes that '\n' returns to column 0.  It could
    #  possibly be more useful for it to return to the initial column
    #  offset.  See comments in requirement assertions.

    # note: not all white space of unicode are represented here, if it
    #  is ever generalized.

    for character in line:
        if character == '\t':
            column = next_tab(column, tab_length)
        elif character == '\r':
            pass
        elif character == '\n':
            column = 0
        else:
            column += 1

    return column

# unit tests
if __name__ == '__main__':

    # for varying starting columns
    for start in range(0, 4):

        # core axiom
        assert column("\t", start) == next_tab(start)

        for count in range(0, 4):

            # a count of spaces
            assert column(" " * count, start) == start + count

            # axiom applied to a count of spaces followed by a tab
            example = " " * count + "\t"
            assert column(example, start) == next_tab(start + count)

    # up to three spaces before an indent
    for n in range(0, 3):
        assert column(" " * count + "\t") == 4 

    # a tab on the first tab stop
    assert column("    \t") == 8

    # newline and linefeed remain untested as unused.

