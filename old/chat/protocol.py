
import os
from urllib import unquote_plus
from twisted.web.http import Request as HTTPRequest
from cixar.python.module_path import module_path
from cixar.ish.sh.protocol import HTTPShellFactory, HTTPShellClientRequest, SessionRequest, SessionService, Session, Mode
from modes import Init as InitBase

class ClientRequest(HTTPShellClientRequest):
    @property
    def log(self):
        # the service is a ChatRoom
        return self.service.log

class ChatRoom(object):
    Request = ClientRequest
    def __init__(self):
        self.chatters = {}
        self.log = []

class Factory(HTTPShellFactory):

    def __init__(self, reactor = None):

        self.chat_room = ChatRoom()

        # each initial mode will need a reference to the
        #  chat service particular to this factory instance.
        #  a global Init function will not suffice, so
        #  we create a new closure for each factory.
        def Init():
            return InitBase(self.chat_room)

        HTTPShellFactory.__init__(
            self,
            Init = Init,
            reactor = reactor,
        )

        self.file_service.next_service = self.chat_room

        # map emoticons into the file service's file hierarchy
        for name in os.listdir(module_path(__file__, 'content', 'tango')):
            self.file_service.contents['.chat/art/tango/' + name] = module_path(
                __file__,
                'content',
                'tango',
                name
            )

# more specific names for imports
ChatClientRequest = ClientRequest
ChatSessionRequest = SessionRequest
ChatSessionService = SessionService
ChatSession = Session
ChatMode = Mode
ChatFactory = Factory

