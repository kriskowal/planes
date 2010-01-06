
from planes.lazy import BaseService, serve, Response, LogService, ResponseService, SessionService
from planes.python.mode import Modal, Mode

class Start(Mode, BaseService):

    def __call__(self, kit, *args, **kws):
        return Response('%s\n' % self.a)

    def start(self):
        print 'here'
        self.a = 10

@serve(port = 8080, debug = True)
@ResponseService
@LogService
@SessionService
def service():
    return Start()

