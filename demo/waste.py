
# Run and browse to http://localhost:8080

from planes.service import serve
from planes.widget import WidgetService
from planes.host import HostService

class Waste(object):
    timeout = 2
    def __html_repr__(self, kit):
        tags = kit.tags
        host = kit.host
        print host(string = 'Hello, World!', expires = False), "won't expire"
        print host(string = 'Hello, World!', timeout = self.timeout)
        return tags.span('In %s seconds, a string will expire.' % self.timeout)

serve(
    HostService(
        WidgetService(Waste()),
        book_keeping_interval = 1
    ),
    port = 8080,
    debug = True,
)

