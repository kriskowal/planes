
# todo factor out chat specific methods of the Mode class, create a mixin

import format
from cixar.ish.sh.protocol import Session as SessionBase, Mode as ModeBase
from cixar.ish.sh.inoculate import inoculate

class Session(SessionBase):
    pass

class Mode(ModeBase):

    emote_handler = format.EmoteHandler(format.emote_table)
    format_handler = format.FormatHandler(format.format_table)

    def broadcast(self, message):
        for chatter in self.chatters.values():
            if chatter.name != self.name:
                try:
                    chatter.session.message(message)
                except:
                    del self.chatters[chatter.name]

    def chat(self, command):
        if command.startswith("/"):
            self.command(command[1:])
        elif not command:
            self.push(Chat(self))
        else:
            self.say(command)

    def say(self, message):
        message = self.emote_handler.transform(
            self.format_handler.transform(inoculate(message)))
        self.message("<font color=blue>%s:</font> %s" %
            (inoculate(self.name), message))
        self.broadcast("<font color=red>%s:</font> %s" %
            (inoculate(self.name), message))

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

        message = self.emote_handler.transform(
            self.format_handler.transform(inoculate(message)))

        self.message("<font color=blue>%s</font> %s" %
            (inoculate(self.name), message))
        self.broadcast("<font color=red>%s</font> %s" %
            (inoculate(self.name), message))

