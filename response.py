
from traceback import *
from planes.python.xml.tags import tags
from itertools import chain
import simplejson

from sys import stderr
try:
    import settings
    stderr = getattr(settings, 'stderr', stderr)
except ImportError:
    pass

class Response(object):

    _code = 200
    _content = ''
    _content_type = 'text/plain'

    def __init__(self, content = None, **kws):

        if content is not None:
            kws.update({'content': content})

        for key, value in kws.items():
            setattr(self, '_' + key, value)

    def __call__(self, request, *args, **kws):
        return self

    def __getattr__(self, key):
        def accessor():
            return getattr(self, '_' + key)
        return accessor

    def __getitem__(self, key):
        return getattr(self, key)

    def headers(self):
        yield ('Content-type', self.content_type())

class Page(Response):

    def content_type(self):
        return 'text/html'

    def content(self):
        return self.html().xml

    def html(self):
        return tags.html(
            self.head(),
            self.body(),
        )

    def head(self):
        title = self.title()
        return tags.head(
            (
                title and
                tags.title(title)
                or None
            ),
            (
                tags.script('', src = script)
                for script in self.scripts()
            ),
            (
                tags.link('', href = style, rel = 'stylesheet', type = 'text/css')
                for style in self.styles()
            ),
            ''
        )

    _title = None

    _scripts = ()

    _styles = ()

    def body(self):
        return tags.body(self.body_content())

    _body_content = None

class Redirect(Response):
    _code = 302

    def __init__(self, location):
        self._location = location

    def headers(self):
        yield ['Location', self.location()]

    _content = ''

class PermanentRedirect(Redirect):
    _code = 301

class NotModified(Response):
    _code = 304

class BadRequest(Response):
    _code = 400

class Restricted(Page):
    _code = 401

    def __init__(self, realm_name, *args, **kws):
        self._realm_name = realm_name
        super(Restricted, self).__init__(self, *args, **kws)

    def headers(self):
        yield ('WWW-Authenticate', 'Basic realm=%s' % repr(self.realm_name()))

class Forbidden(Response):

    def __init__(self, realm_name, *args, **kws):
        self._realm_name = realm_name
        super(Restricted, self).__init__(self, *args, **kws)

    _code = 403

class NotFound(Page):
    _code = 404

    def __init__(self, path, *args, **kws):
        self._path = path
        super(NotFound, self).__init__(self, *args, **kws)

    def path(self):
        return self._path

    def body_content(self):
        return (
            tags.h1('Not Found'),
            tags.p(self.path())
        )

class NotAllowed(Response):
    _code = 405
    _permits = ['GET', 'POST']

class Gone(Response):
    _code = 410

class ServerError(Response):
    _code = 500

class Index(Page):

    _footer = None,

    def __init__(self, path, paths):
        self._path = path
        self._paths = paths

    def title(self):
        return self.path()

    def body_content(self):
        return (
            self.header(),
            self.path_table(),
            self.footer(),
        )

    def header(self):
        return tags.h1(self.path())

    def path_table(self):
        parent = []
        if self.path() != '/':
            parent.append(['..', '..'])
        return tags.ul(
            self.path_row(*path)
            for path in chain(
                parent,
                self.paths().items()
            )
        )

    def path_row(self, href, file_name):
        return tags.li(tags.a(href, href = href))

class ResponseService(object):

    def __init__(self, service, debug = False):
        self.service = service
        self.debug = debug

    def send_response(self, request, response):
        write = request.start_response(response.code(), response.headers())
        write(response.content())
        request.finish()

    def __call__(self, request, *args, **kws):
        try:
            response = self.service(request, *args, **kws)
            if response is not None:
                if isinstance(response, Response):
                    self.send_response(request, response)
                else:
                    self.send_response(request, Response(str(response)))
        except Exception, exception:
            if request.debug:
                print_stack(file = stderr)
                print>>stderr, '----- page caught here ----'
                print_exc(file = stderr)
                print>>stderr, '503 - %s' % request.full_path

            self.send_response(request, Page(
                code = 503,
                body_content = (
                    tags.h1('Server Error'),
                    str(exception.__class__.__name__),
                    ': ',
                    str(exception)
                )
            ))
            raise

