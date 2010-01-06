"""
"""

from pprint import pformat

class Modal(object):
    """
    """

    __inited = False

    def __init__(self, Mode = None, *args, **kws):
        """
        """
        self.__inited = True
        self.modes = []
        if Mode is not None:
            self.Mode = Mode
        if self.Mode is not None:
            self.push(self.Mode())
        super(Modal, self).__init__(*args, **kws)

    # todo: create observable event properties
    def on_start(self, mode):
        """
        """
        pass
    def on_stop(self, mode):
        """
        """
        pass
    def on_pause(self, mode):
        """
        """
        pass
    def on_resume(self, mode):
        """
        """
        pass
    def on_exit(self):
        """
        """
        pass

    def goto(self, mode):
        """
        """

        # effectively, a push followed by a pop, except the parent mode
        #  does not resume, nor pause

        self.on_stop(self.mode)
        if hasattr(self.mode, '_stop'):
            self.mode._stop()
        self.modes.pop()

        mode.modal = self

        self.modes.append(mode)
        self.on_start(mode)
        if hasattr(mode, '_start'):
            mode._start()

    def push(self, mode):
        """
        """

        mode.modal = self

        if len(self.modes) > 0:
            self.on_pause(self.mode)
            if hasattr(mode, '_pause'):
                self.mode._pause()
        self.modes.append(mode)
        self.on_start(mode)
        if hasattr(mode, '_start'):
            if hasattr(mode, '_start'):
                mode._start()

    def pop(self):
        """
        """
    
        self.on_stop(self.mode)
        if len(self.modes) == 1: self.on_exit()
        if hasattr(self.mode, '_stop'):
            self.mode._stop()
        self.mode.modal = None
        self.modes.pop()

        if len(self.modes) > 0:
            self.on_resume(self.mode)
            if hasattr(self.mode, '_resume'):
                self.mode._resume()

    def exit(self):
        """
        """
        while len(self.modes) > 0:
            self.pop()

    @property
    def mode(self):
        return self.modes[-1]

class Mode(object):
    """
    Mode is a base class for modal 'states'.
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
        topmost mode on the modal's stack of modes.
        """
        return self.modal.mode == self

    def __init__(self, process = None):
        """
        """
        self.modal = None
        if process is not None:
            self.run = lambda: process

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
                self.modal.push(mode)
            else:
                self.start()
        except StopIteration:
            self.modal.pop()

