
def ShellService():
    service = SessionService(service)





# status: deprecated

from planes.javascript import Javascript, javascripts
from planes.python.mix import mix
from planes.python.mode import Modal, Mode as ModeBase
from planes.python.html import Kit
from planes.python.xml.tags import tags

from planes.lazy import (
    PathService, SessionService, CommService,
    MessageBufferService, MessageBufferWidget,
    CommandBoxWidget,
)

class Mode(ModeBase):

    prompt = ':'

    def start(self):
        self.queue.append(('prompt', self.prompt))
        super(Mode, self).start()
    def resume(self):
        self.queue.append(('prompt', self.prompt))
        super(Mode, self).resume()
    def stop(self):
        self.queue.append(('prompt', ''))
        super(Mode, self).stop()

    def command(self, text):
        kit = self.kit
        tags = kit.tags
        self.message((
            'Sorry, this ', tags.b('service'), ' is ',
            tags.b('not ready'), '.  ',
            'The administrator has not finished configuring ',
            'this service properly.'
        ))

class Session(CommService, Modal):

    def Mode(self):
        return self.service.Mode()

    def __init__(self, service, **keywords):
        self.service = service
        self.queue = []
        self.cookies = []
        super(Session, self).__init__(**keywords)

    def message(self, message):
        self.queue.append(('message', tags.div(message).xml))

    def add_cookie(self, key, value):
        self.cookies.append((key, value))

    def push(self, mode):
        mode.__class__ = mix(mode.__class__, Mode)
        super(Session, self).push(mode)

    def comm_output(self, kit, input):

        tags = kit.tags
        self.kit = Kit(kit, service = self.service)

        self.tick()

        for element in input.elements:
            if element.name == 'command':
                if element.elements:
                    command = element.elements[0]
                    self.command(command)

        for key, value in self.cookies:
            kit.request.addCookie(key, value)
        self.cookies = []

        result = (tags[name](content) for name, content in self.queue)
        self.queue = []
        return result

class ClientService(MessageBufferService):
    def __init__(self, session_service, body = None, **keywords):
        self.session_service = session_service
        if body is not None:
            self.shell_body = lambda kit: kit.html_repr(body)
        super(ClientService, self).__init__(**keywords)
    def shell_body(self, kit):
        pass
    def message_buffer_body(self, kit):
        tags = kit.tags
        id = kit.next_id()
        command_id = '%s_command' % id
        prompt_id = '%s_prompt' % id
        return tags.div(
            tags.table(
                tags.tr(
                    tags.td(
                        tags.nobr('', id = prompt_id),
                        style = 'vertical-align: bottom;'
                    ),
                    tags.td(
                        CommandBoxWidget(id = command_id),
                        style = 'width: 100%'
                    ),
                ),
                style = '''
                    width: 100%;
                '''
            ),
            Javascript(
                '''shell.open(
                    %s, %s, %s,
                    document.getElementsByTagName('body')[0]
                );''' % (
                    repr(self.session_service.base_path),
                    repr(prompt_id),
                    repr(command_id),
                ),
                {'shell': javascripts.shell,}
            ),
            self.shell_body(kit),
        )

class Service(PathService):

    ClientService = ClientService
    Mode = Mode

    def Session(self):
        result = Session(self)
        return result

    def __init__(self, body = None, **keywords):
        session_service = SessionService(
            self.Session,
            timeout = 20
        )
        service = self.ClientService(session_service, body)
        keywords['service'] = service
        keywords['contents'] = {
            'session': session_service,
        }
        super(Service, self).__init__(**keywords)

class Widget(MessageBufferWidget):

    def Session(self):
        return Session(self)

    def __init__(self, Session = None, body = None):
        if Session is not None:
            self.Session = Session
        if body is not None:
            self.shell_body = lambda kit: kit.html_repr(body)

    def shell_body(self, kit):
        pass

    def message_buffer_body(self, kit):
        tags = kit.tags
        id = kit.id
        host = kit.host
        debug = kit.debug

        command_id = '%s_command' % id
        prompt_id = '%s_prompt' % id

        session = self.Session()
        host(service = session, timeout = 20)

        return tags.div(
            tags.table(
                tags.tr(
                    tags.td(
                        tags.nobr('', id = prompt_id),
                        style = 'vertical-align: bottom;'
                    ),
                    tags.td(
                        CommandBoxWidget(id = command_id),
                        style = 'width: 100%'
                    ),
                ),
                style = '''
                    width: 100%;
                '''
            ),
            Javascript(
                "shell.open(%s, %s, %s, %s, {'debug': %s});" % (
                    repr(session.base_path),
                    repr(prompt_id),
                    repr(command_id),
                    repr(id),
                    debug and '1' or '0'
                ),
                {'shell': javascripts.shell,}
            ),
            self.shell_body(kit),
        )

ShellMode = Mode
ShellSession = Session
ShellService = Service
ShellClientService = ClientService
ShellWidget = Widget

