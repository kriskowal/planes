
# 2004-08-07 created, Kris Kowal

from tab_length import tab_length

def next_tab(column, tab_length = tab_length):
    """
        returns the |column| offset of the tab stop that immediately succeeds
        the given |column| offset, given tab stops at equal intervals of
        |tab_length|.  |tab_length| must be a power of two.

        mathematically equivalent but faster than:
        =>
            tab_length * int(column / tab_length + 1)
            where tab_length is a power of 2

    """
    return (column & ~(tab_length - 1)) + tab_length

# unit test
if __name__ == '__main__':

    next_tab_actual = next_tab

    # note: the following implementation is more robust, but much slower.
    #  consider using it instead if a perverse use case comes up.

    def next_tab(column, tab_length = tab_length):
        return tab_length * int(column / tab_length + 1)

    # these cases fail for next_tab_actual.
    assert next_tab(0, 3) == 3
    assert next_tab(3, 3) == 6

    # verify next_tab against next_tab_actual
    for column in range(0, 8):
        assert next_tab(column) == next_tab_actual(column)

    # boundary conditions
    assert next_tab(tab_length - 1) == tab_length
    assert next_tab(tab_length) == tab_length * 2

