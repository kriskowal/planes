
from planes.lazy import serve, function_service as service, PathService

from planes.page import Redirect

@service()
def redirect(self, *args):
    return Redirect(self.base_path + '/hello' + self.path)

@service(content_type = 'text/plain')
def hello(self, who = 'World'):
    return 'Hello, %s!' % who

serve(
    port = 8080,
    interface = '',
    service = PathService(
        contents = {
            'hello': hello
        },
        next_service = redirect,
    ),
)

