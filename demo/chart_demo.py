
# Run ./pyshd chart_demo.py
# and browse to https://localhost:2380
# requires your system credentials
# try the command "foograph"
# requires SSL and AuthShadow

from planes.python.graphkit import *
from planes.python.imagekit import *
from planes.python.tablekit import *
from planes.python.inspectkit import *
from planes.python.chartkit import *

# graph demo components
class Joe(object): pass
class Bob(Joe): pass
class Bill(Joe): pass
class Warren(Bob, Bill): pass
class Phil(Warren): pass
class Gosh(Phil, Bill): pass
class Foo(Gosh): pass

foograph = classgraph(Foo)

