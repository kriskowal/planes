
from sys import stderr

def color(color):
    stderr.write("\x1b[%dm" % color)
    stderr.flush()

def clear():
    color(0)

def red():
    color(31)

def green():
    color(32)

def yellow():
    color(33)

def blue():
    color(34)

