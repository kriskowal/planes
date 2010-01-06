
from planes.lazy import PathService, JsonRequestService
import simplejson

class JsonConnectionService(PathService):

    def __init__(self):

        self.messages = []
        self.requests = []
        self.new = True

        def post_service(request):
            self.receive(request.path[1:])
            request.finish()

        @JsonRequestService
        def post_json_service(request, object):
            self.requests.insert(0, request)
            self.requests[2:] = []
            if request.session_lost:
                self.new = True
            self.receive(object['message'])
            self.flush()

        def push_service(request):
            self.requests.insert(0, request)
            self.requests[2:] = []
            if request.session_lost:
                self.new = True
            self.flush()

        super(JsonConnectionService, self).__init__(
            paths = {
                'post': post_service,
                'post.json': post_json_service,
                'push.json': push_service,
            },
        )

    def get_messages(self):
        response = {
            'new': self.new,
            'messages': list(self.messages),
        }
        self.messages[:] = []
        self.new = False
        return response

    def flush(self):
        if self.requests and (self.messages or self.new):
            request = self.requests.pop(0)
            response = self.get_messages()
            request.output.write(simplejson.dumps(response))
            request.finish()

    def send(self, message):
        self.messages.append(message)
        self.flush()

    def receive(self, message):
        pass

