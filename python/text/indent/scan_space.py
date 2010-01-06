
def scan_space(line):
    """
        returns the index of the first non-space character in a string
    """

    # note: as used in indent.shift(...), |isspace| does more work than
    #  is necessary.  This function could assume that it won't ever
    #  read a '\n', '\r' nor any other space character.

    index = 0
    while index < len(line) and line[index].isspace(): index += 1
    return index

# unit tests
if __name__ == '__main__':

    for assertion in [
        ("", 0),
        (" ", 1),
        ("\t", 1),
        (" a", 1),
        ("\ta", 1)
    ]:
        assert scan_space(assertion[0]) == assertion[1]

