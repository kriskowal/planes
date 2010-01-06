
# status: deprecated

from http import HttpService, HttpRequest
from javascript import Javascript, javascripts

class Service(HttpService):

    def __init__(self, body = None, **keywords):
        if body is not None:
            self.message_buffer_body = body
        super(MessageBufferService, self).__init__(**keywords)

    def message_buffer_body(self, kit):
        pass

    class Request(HttpRequest):

        def body(self):
            service = self.service
            kit = self.kit
            return (
                kit.html_repr(
                    Javascript(
                        '''
                            var body = document.getElementsByTagName('body')[0];
                            messageBuffer.init(body, {'debug': 1});
                        ''',
                        {'messageBuffer': javascripts.message_buffer,},
                    ),
                ),
                service.message_buffer_body(kit)
            )

class Widget(object):

    def __init__(self, body = None, **keywords):
        if body is not None:
            self.message_buffer_body = body
        super(Widget, self).__init__(**keywords)

    def message_buffer_body(self, kit):
        pass

    def __html_repr__(self, kit):
        host = kit.host
        tags = kit.tags
        kit.id = kit.next_id()
        return tags.div(
            Javascript(
                "messageBuffer.init(%s, {'debug': 1})" % repr(kit.id),
                {'messageBuffer': javascripts.message_buffer,}
            ),
            self.message_buffer_body(kit),
            id = kit.id,
            style = '''
                overflow: auto;
                padding: 10px;
                margin: 0px;
                width: 90%;
                height: 90%;
                outline: outset 1px;
            '''
        )

MessageBufferService = Service
MessageBufferWidget = Widget

