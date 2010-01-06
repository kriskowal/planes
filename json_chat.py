
from planes.lazy import Kit, SessionService,\
    FunctionService, JsonWriterService,\
    LogService, ResponseService, PathService
from planes.response import Redirect
from weakref import WeakValueDictionary

class User(Kit):
    def read(self):
        result = self.messages
        self.messages = []
        return result
    def message(self, message):
        self.messages.append(message)

def JsonChatService():

    users = WeakValueDictionary()

    def next_name(name = 'Annonymous'):
        if name not in users:
            return name
        else:
            n = 0
            while True:
                consider = "%s%s" % (name, n)
                if consider not in users:
                    return consider
                n += 1

    def broadcast(user_name, message):
        for other_user_name, user in users.items():
            user.message([user_name, message])

    @SessionService
    def session_service():

        name = next_name()
        user = User(
            name = name,
            messages = []
        )
        users[name] = user
        
        @JsonWriterService
        @FunctionService
        def control(kit, message = None, name = None, logout = None):
            if message is not None:
                broadcast(user.name, message)
            if name is not None:
                user.name = name
                users[user.name] = user
            if logout is not None:
                kit.session.logout()
                
            return {
                'session_id': kit.session_id,
                'user_name': user.name,
                'users': users.keys(),
                'messages': user.read(),
            }

        return control

    root = Redirect('root')

    service = PathService(
        service = root,
        paths = {
            'chat': session_service,
        },
    )

    service = ResponseService(service)
    service = LogService(service)
    return service

