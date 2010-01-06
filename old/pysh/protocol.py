
from planes.python.module_path import module_path
from planes.python.wrap import wrap
from planes.sh.protocol import Factory as BaseFactory, SessionRequest, SessionService, ClientRequest as BaseClientRequest, ClientService as BaseClientService
from planes.host import Host
from planes.auth_shadow_self import AuthShadowSelfService
from session import Session, Mode
from modes import Init as BaseInit

class ClientRequest(BaseClientRequest):
    @property
    def css_files(self):
        for css_file in BaseClientRequest.css_files:
            yield css_file
        yield '.pysh/' + '@.css'

class ClientService(BaseClientService):
    Request = ClientRequest

class Factory(BaseFactory):

    ClientService = ClientService
    Host = Host

    def __init__(self, authenticate = True, *arguments, **keywords):

        BaseFactory.__init__(self, *arguments, **keywords)

        self.file_service.contents['.pysh/' + '@.css'] = module_path(
            __file__,
            'content',
            '@.css'
        )

        self.host = self.Host('.adhoc')
        self.path_service['.adhoc'] = self.host
        self.client_service = self.ClientService()
        self.file_service.next_service = self.client_service

        # require basic HTTP authentication against the unix
        #  password repository for the user that runs
        #  pyshd.
        if authenticate:
            self.service = AuthShadowSelfService(self.service)

    def Init(self, *arguments, **keywords):
        return BaseInit(host = self.host, *arguments, **keywords)

# specific names for imports
PythonHTTPShellFactory = Factory
PythonHTTPShellSession = Session
PythonHTTPShellMode = Mode
PythonHTTPShellSessionRequest = SessionRequest
PythonHTTPShellSessionService = SessionService

