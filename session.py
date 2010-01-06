
from planes.lazy import AdhocDict, BaseService
from planes.kit import Kit

class Session(Kit):

    def __init__(self, session_service, id, service, expiration):
        self.session_service = session_service
        self.id = id
        self.service = service
        self.expiration = expiration

    def logout(self):
        self.session_service.logout(self.id)

class SessionService(BaseService):
    def __init__(self, Service):
        self.Service = Service
        sessions = AdhocDict()
        sessions.length = 6
        self.sessions = AdhocDict() 

    def logout(self, id):
        del self.sessions[id]
    
    def __call__(self, kit, *args, **kws):
        sessions = self.sessions
        Service = self.Service
        request = kit.request

        session_id = request.getCookie('session_id')
        session_exists = (
            session_id is not None and # this is the way it probably
                                       # will be if it's ever fixed.
            session_id != 'None' # this is the way it is
                                 # at the time of writing.
        )

        if (
            session_exists and
            session_id in sessions
        ):
            kit.session_lost = False
            session = sessions[session_id]
        else:
            kit.session_lost = session_exists
            session_id = sessions.getkey()
            service = Service()
            session = Session(
                self,
                session_id,
                service,
                0
            )
            service.session_service = self
            service.session = session
            request.addCookie('session_id', session_id)
            sessions[session_id] = session

        kit.session_id = session.id
        kit.session = session
        service = session.service
        return service(kit, *args, **kws)

