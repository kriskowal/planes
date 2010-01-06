
"""
    Utilities for measuring and trimming indentation.
"""

# 2004-08-07 refactored
# 2004-05-30 created, Kris Kowal

from tab_length import *
from scan_space import *
from column import *
from next_tab import *
from measure import *
from shift import *
from shift_iter import *
from width import *

from planes.python.peekable import peekable
line_shift = shift

class ShiftError(Exception): pass

def lines(source):
    if isinstance(source, str):
        for line in source.split("\n"):
            yield line.rstrip()
    else:
        for line in source: yield source

def shift(source, depth = tab_length):
    initial = 0
    start = 0
    source = peekable(lines(source))
    result = "\n".join(shift_iter(source, initial, start, tab_length, depth))
    return result

