"""
Utility functions.
"""

def convert_intervals(value, source_start, source_end, dest_start, dest_end):
    """
    Coverts a value in the source interval to the corresponding value
    in the destination interval.

    This function won Aradin's nomination for MVF (Most Valuable Function)
    in game programming.
    """
    x = float(value)
    a, b = float(source_start), float(source_end)
    c, d = float(dest_start), float(dest_end)
    #print x
    #print a, b
    #print c, d
    #print x - a
    #print (x - a) / (a - b)
    #print (x - a) / (a - b) * (c - d)
    #print (x - a) / (a - b) * (c - d) + c
    return type(x)( (x - a) / (a - b) * (c - d) + c )
 
def clamp(value, max = None, min = None):
    """
    Keeps a value from going over or under the given constraints.
    """
    ret = value
    if max is not None:
        if value > max:
             ret = max

    if min is not None:
        if value < min:
            ret = min

    return ret