
"""

It's worth noting why this file exists before brave
refactorors boldly attempt to eliminate the
waste, for good or ill.  This file parallels other
HTTPShell derivations and serves the purpose of
maintaining orthogonzlity alone.  However, this file
also provides a conduit for Session and Mode definitions
to flow into the protocol module and avoids certain
cyclic import problems.

protocol <--------------------- sh.protocol (Factory, ...)
                     session <- sh.protocol (Session, Mode)
protocol <---------- session (Session, Mode)
         <- modes <- session (Mode)
protocol <- modes (Init)

"""

from planes.sh.protocol import Session, Mode

