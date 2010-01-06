
import os
import cixar.ish
from cixar.python.module_path import module_path
from cixar.ish.sh.command import Commands
from cixar.ish.sh.inoculate import inoculate
from session import Mode

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

class Common(Mode):

    name_cookie_key = 'chat.name' # sketchy, might want to create a site based cookie name scheme

    def set_name(self, name):
        self.cookie(self.name_cookie_key, name)
        name = next_name(self.chatters, name)
        del self.chatters[self.name]
        self.chatters[name] = self
        self.name = name

    @property
    def chat_room(self):
        return self.service
    @property
    def chatters(self):
        return self.chat_room.chatters

class Chat(Common):

    title = 'Chat'
    prompt = '"'
    commands = Commands()

    def __init__(self, init):
        self.service = init.service
        self.name = init.name
        super(Chat, self).__init__()

    def command(self, command):
        if command.startswith('/'):
            super(Chat, self).command(command[1:])
        else:
            self.say(command)

    def start(self):
        super(Chat, self).start()
        self.chatters[self.name] = self
        self.emote('enters')
        self.command('/who')

    def stop(self):
        self.emote('exits')
        del self.chatters[self.name]
        super(Chat, self).stop()

    def broadcast(self, message):
        self.log(message)
        super(Chat, self).broadcast(message)

    def log(self, message):
        self.chat_room.log.append(message)

class Init(Common):

    Chat = Chat

    def __init__(self, service):
        self.service = service
        super(Init, self).__init__()

    def process(self, http_request):

        service = self.service

        # get the desired name from a cookie
        name = http_request.getCookie(self.name_cookie_key)
        if name is not None:
            name = self.name = next_name(self.chatters, name)
        # or get a default name
        else:
            name = next_name(self.chatters)
        self.name = name
        self.chatters[name] = self

        self.message(
            '<p>You are <font color="blue">%s</font>.</p>' % (
                inoculate(self.name)
            )
        )
        self.broadcast(
            '<p><font color="red">%s</font> enters.</p>' % (
                inoculate(self.name)
            )
        )

        self.goto(self.Chat(self))

    def process(self, request):
        print self.name

Chat.commands.load(*(
    module_path(cixar.ish, *file_name)
    for file_name in (
        ('sh', 'general_commands.py'),
        ('chat', 'commands.py'),
        ('chat', 'socials.py'),
    )
))

