
# 2004-02-19 integrated with the traversal algorithm.  Modified
#  the parameters to accommodate practical edge cases.
# 2004-08-07 reiterated to accommodate variant starting column requirements
# 2004-05-30 created as indent.py, Kris Kowal

# status: works, need test cases for initial, start, and tab_length
#  variations.

from tab_length import tab_length
from next_tab import next_tab
from scan_space import scan_space
from column import column

def shift(line, initial = 0, start = 0, tab_length = tab_length, depth = None):
    """
        in short, shifts a line left one tab_length by axing the first
         tab.

        Of course, the world isn't that simple.  There are tabs to
         be accounted for, and various desirable behaviors if the resulting
         string doesn't have enough white space.
         
        So, this algorithm really shifts the indentation of a given |line|
         by |tab_length|, preserving the existing order of spaces and tabs
         as much as possible.  If |line| is blank, returns as much of the
         space that exists after |start| plus one |tab_length|.  If shifting
         this much white space off would cause a dark character to fall
         behind this column, returns |None|.
        |initial| is the column on which the |line| begins (for cases
         where the line implicitly succeeds some other content).
        |start| is the column number past |initial| at which the returned
         string should begin on.
        |tab_length| must be a power of two.
    """

    if depth is None:
        depth = tab_length

    # verily, tabs are a finicky breed.  Like an inch worm, as a string
    #  of mixed spaces shifts, its front and back dance with one another.
    #  this function is perilous.  Edit with extreme diligence and
    #  at your peril.

    # separate the line into its space and content portions
    index = scan_space(line)
    space, content = line[:index], line[index:]

    # determine what column the newly shifted line should begin on
    goal = column(space, initial, tab_length) - depth
    
    # if shifting the line one |tab_length| would regress the string
    #  of white space before |start|
    if goal < start:
        # blank lines are special
        if not len(content): return ""
        # report that the line was unshiftable otherwise
        else: return None
    
    # convert tabs into spaces if necessary
    # todo: consider optimizing
    for at in range(0, start + depth):
        if space[at] == '\t':
            equivalent = ' ' * (next_tab(initial + at) - (initial + at))
            space = space[:at] + equivalent + space[at+1:]
    
    # chew off a width worth of spaces.
    space = space[start + depth:]

    assert column(space, initial + start, tab_length) == goal
    return space + content

if __name__ == '__main__':

    # base cases

    assert shift("a") == None
    assert shift(" a") == None
    assert shift("  a") == None
    assert shift("   a") == None
    assert shift("    a") == "a"
    assert shift("     a") == " a"

    assert shift("\ta") == "a"
    assert shift(" \ta") == "a"
    assert shift("  \ta") == "a"
    assert shift("   \ta") == "a"
    assert shift("    \ta") == "\ta"

    assert shift("\ta") == "a"
    assert shift("\t a") == " a"
    assert shift("\t  a") == "  a"
    assert shift("\t   a") == "   a"
    assert shift("\t    a") == "    a"


    # blank lines

    # spaces

    # in recess
    assert shift("") == ""
    assert shift(" ") == ""
    assert shift("  ") == ""
    assert shift("   ") == ""
    assert shift("    ") == ""
    
    # in excess
    assert shift("     ") == " "
    assert shift("      ") == "  "

    # tabs

    # in recess
    assert shift("") == ""
    assert shift(" ") == ""
    assert shift("\t") == ""
    
    # in excess
    assert shift("\t ") == " "
    assert shift("\t\t") == "\t"
    assert shift("\t  \t") == "  \t"
    assert shift("  \t \t ") == " \t "

    # spot check
    assert shift("\t\ta", 2) == "  a"
    assert shift("\t   \ta", 2) == " \ta"
    assert shift("   \ta", -2) == "  a"
    
    # assure "modify only beginning" behavior
    assert shift("\t\t\ta", 2) == "  \ta"

    # todo: tab_length variation tests

