"""
Provides a framework for cooperative task management
with generators.
"""

from pprint import pformat

class Session(object):
    """
    """

    def __init__(self, InitialMode = None):
        """
        """
        self.modes = []
        if InitialMode is not None:
            self.push(InitialMode())

    # todo: create observable event properties
    def onStart(self, mode):
        """
        """
        pass
    def onStop(self, mode):
        """
        """
        pass
    def onPause(self, mode):
        """
        """
        pass
    def onResume(self, mode):
        """
        """
        pass
    def onExit(self):
        """
        """
        pass

    def goto(self, mode):
        """
        """

        # effectively, a push followed by a pop, except the parent mode
        #  does not resume, nor pause

        self.onStop(self.modes[-1])
        self.modes[-1]._stop()
        self.modes.pop()

        mode.session = self

        self.modes.append(mode)
        self.onStart(mode)
        mode._start()

    def push(self, mode):
        """
        """

        mode.session = self

        if len(self.modes) > 0:
            self.onPause(self.modes[-1])
            self.modes[-1]._pause()
        self.modes.append(mode)
        self.onStart(mode)
        mode._start()

    def pop(self):
        """
        """

    
        self.onStop(self.modes[-1])
        if len(self.modes) == 1: self.onExit()
        self.modes[-1]._stop()
        self.modes[-1].session = None
        self.modes.pop()

        if len(self.modes) > 0:
            self.onResume(self.modes[-1])
            self.modes[-1]._resume()

    def exit(self):
        """
        """
        while len(self.modes) > 0:
            self.pop()
            
    def __getattr__(self, name):
        """
        """
        if len(self.modes) > 0:
            if hasattr(self.modes[-1], name):
                return getattr(self.modes[-1], name)
        raise AttributeError(
            "%s object has not attribute %s" % (
                pformat(self.__class__.__name__),
                pformat(name)
            )
        )

class Mode(object):
    """
    Mode is a base class for session 'states'.
    """

    def run(self):
        """
        """
        pass
    def start(self):
        """
        """
        pass
    def stop(self):
        """
        """
        pass
    def tick(self):
        """
        """
        pass
    def pause(self):
        """
        """
        pass
    def resume(self):
        """
        """
        pass

    @property
    def running(self):
        """
        Provides a read-only property to answer whether this
        mode is 'running'.  A mode is running iff it is the
        topmost mode on the session's stack of modes.
        """
        return self.session.modes[-1] == self

    def __init__(self, process = None):
        """
        """
        self.session = None
        if process is not None:
            self.run = lambda: process

    def __getattr__(self, name):
        """
        """
        if (
            self.session is not None and
            hasattr(self.session, name)
        ):
            return getattr(self.session, name)
        else:
            raise AttributeError(
                "%s object has not attribute %s" % (
                    pformat(self.__class__.__name__),
                    pformat(name)
                )
            )

    def _start(self):
        """
        """
        self._process = self.run()
        if self._process is None:
            self.start()
        else:
            self._next()

    def _resume(self):
        """
        """
        if self._process is None:
            self.resume()
        else:
            self._next()

    def _stop(self):
        """
        """
        self.stop()

    def _pause(self):
        """
        """
        self.pause()

    def _next(self):
        """
        """
        try:
            mode = self._process.next()
            if mode is not None:
                self.session.push(mode)
            else:
                self.start()
        except StopIteration:
            self.session.pop()

