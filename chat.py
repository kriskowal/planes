
from planes.lazy import ShellService, ShellSession, inoculate
from planes.python.xml.tags import tags

def next_name(chatters, name = 'Annonymous'):
    if name not in chatters:
        return name
    else:
        n = 0
        while True:
            consider = "%s%s" % (name, n)
            if consider not in chatters:
                return consider
            n += 1

class Mode(object):

    prompt = '"'

    def __init__(self, service):
        self.service = service
        self.name = next_name(self.service.chatters)
        self.service.chatters[self.name] = self

    def chat(self, text):
        if text.startswith("/"):
            super(Mode, self).command(text[1:])
        elif not text:
            self.push(super(Mode, self)(self))
        else:
            self.say(text)

    command = chat

    def start(self):
        self.emote('enters.')
    def stop(self):
        self.emote('exits.')

    def broadcast(self, message):
        for chatter in self.service.chatters.values():
            if chatter.name != self.name:
                try:
                    chatter.message(message)
                except:
                    del self.service.chatters[chatter.name]
                    raise

    def say(self, message):
        self.message((tags.font(self.name, ':', color = 'blue'), ' ', message))
        self.broadcast((tags.font(self.name, ':', color = 'red'), ' ', message))

    def emote(self, message):

        # treat the message
        message = message.strip()

        # implicit punctuation
        if not (
            message.endswith('.') or
            message.endswith('?') or
            message.endswith('!')
        ):
            message = '%s.' % message

        self.message(tags.font(self.name, ' ', message, color = 'blue'))
        self.broadcast(tags.font(self.name, ' ', message, color = 'red'))

class Session(ShellSession):
    pass

class Service(ShellService):

    def Session(self):
        return Session(self)

    def Mode(self):
        return Mode(self)

    def __init__(self, **keywords):
        super(Service, self).__init__(**keywords)
        self.chatters = {}
        self.log = []

ChatService = Service
ChatSession = Session
ChatMode = Mode

