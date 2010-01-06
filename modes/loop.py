
from session import Mode

class Loop(Mode):
    def __init__(self, mode):
        super(Loop, self).__init__()
        self.mode = mode
    def run(self):
        while True:
            yield self.mode

