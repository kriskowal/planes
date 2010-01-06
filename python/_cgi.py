"""
    An echo of the native Python CGI module
    so that it can be imported from within
    the planes module (which has its own 
    cgi module and doesn't mean itself when
    it imports cgi).
"""
from cgi import *
