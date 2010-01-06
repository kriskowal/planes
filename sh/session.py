"""\
HTTPShell Session and Mode classes

This file exists only to satisfy orthogonality with
other modules that keep Session and Mode
classes outside the protocol file, most notably
the planes.python.session module wherein the Session
and Mode base classes are defined.  Session and Mode
are in fact defined in the nearby protocol module
wherein they are tightly coupled with other 
protocol classes.

"""

from protocol import Session, Mode

