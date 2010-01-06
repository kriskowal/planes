
from scan_space import scan_space
from column import column

def measure(line, start = 0):
    """
        returns the column number of the first non-white character on |line|
        assuming that |line| begins at column |start|.
    """
    index = scan_space(line)
    return column(line[:index], start)
