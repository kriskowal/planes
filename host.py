
from planes.path import PathService, PathRequest
from planes.http import HttpService, HttpRequest
from weakref import proxy
from time import time

class Request(PathRequest):
    pass

class Service(PathService):

    Request = Request
    book_keeping_interval = 1
    timeout = 10

    def __init__(
        self,
        next_service = None,
        contents = None,
        service = None,
        reactor = None,
        handlers = None,
        **keywords
    ):

        keywords['contents'] = contents
        keywords['service'] = service
        keywords['next_service'] = next_service

        self._service = None
        self._next_service = None

        super(Service, self).__init__(**keywords)

        # let all of the subcontained services know they can use this
        #  host
        if service in self.contents.values() + [service, next_service]:
            if service is not None and service.host is None:
                service.host = self

        if not handlers:
            handlers = (
                HandleFile(),
                HandleFileName(),
                HandleString(),
                HandleRef(),
                HandleFunction(),
                HandleService(),
            )
        self.handlers = {}
        self.handlers.update((handler.keyword, handler) for handler in handlers)

        if reactor is None:
            from twisted.internet import reactor

        self.reactor = reactor

        # arrange for old content to expire
        self.book = []
        self.booked_paths = set()
        def book_keeping_loop():
            self.book_keeping()
            self.reactor.callLater(
                self.book_keeping_interval,
                book_keeping_loop
            )
        book_keeping_loop()

    def book_keeping(self):
        for handler in self.handlers.values():
            if hasattr(handler, 'book_keeping'):
                handler.book_keeping()
        
        # remove expired content
        now = time()
        while self.book:
            path, expiration = self.book[0]
            if expiration < now:
                if path in self.contents:
                    # recheck the expiration time in case the
                    # service has been last_access
                    service = self.contents[path]
                    if hasattr(service, 'last_access'):
                        expiration = service.last_access + service.timeout
                    if expiration < now:
                        base_path = service.base_path
                        print base_path, 'expired'
                        self.release_path(path)
                        self.booked_paths.discard(path)
                self.book.pop(0)
            else:
                # only traverse as deep in the list as the
                # last expiration time recorded that is less
                # than the current time.
                break

    def touch(self, path):
        if path in self.booked_paths:

            now = time()
            service = self.contents[path]

            if hasattr(service, 'last_access'):
                service.last_access = now
            else:
                self.book = [
                    (book_path, expiration)
                    for book_path, expiration in self.book
                    if book_path != path
                ]

            # todo: use the service's timeout variable if it has one
            self.book.append((path, now + self.timeout))

    def add(self, handler):
        self.handlers[handler.keyword] = handler

    def handler(self, file = None, **keywords):

        if file is not None:
            keywords['file'] = file

        # find an eligible host object for the given heywords
        candidates = set(keywords.keys()).intersection(set(self.handlers.keys()))
        original_candidates = set(candidates)
        for candidate in original_candidates:
            obviates = self.handlers[candidate].obviates
            for obviate in obviates:
                if obviate in candidates:
                    candidates.remove(obviate)

        if len(candidates) == 0:
            raise NoHandlerError("No candidates")
        elif len(candidates) > 1:
            raise AmbiguousHandlerError("Too many candidates")
        
        handler = self.handlers[candidates.pop()]

        return handler

    def reserve_path(self, *arguments, **keywords):
        try:
            handler = self.handler(*arguments, **keywords)
            if hasattr(handler, 'reserve_path'):
                return handler.reserve_path(self, *arguments, **keywords)
        except NoHandlerError:
            pass
        return super(Service, self).reserve_path(*arguments, **keywords)

    def use_path(self, path, content):
        content.host = self
        return super(Service, self).use_path(path, content)

    def host(self, *arguments, **keywords):
        handler = self.handler(*arguments, **keywords)
        return handler(self, **keywords)

    __call__ = host

    def get_service(self):
        return self._service
    def set_service(self, service):
        self._service = service
        service.parent_service = self
        service.host = self
    service = property(get_service, set_service)

    def get_next_service(self):
        return self._next_service
    def set_next_service(self, next_service):
        self._next_service = next_service
        next_service.host = self
    next_service = property(get_next_service, set_next_service)

# todo: integrate PollService so 

class HandleService(object):
    keyword = 'service'
    obviates = []

    def __call__(
        self,
        host,
        service,
        expires = None,
        timeout = None,
        path = None,
        **ignored
    ):

        if expires is None:
            expires = False
        if timeout is None:
            timeout = host.timeout

        if path is None:
            path = host.reserve_path(length = 6)

        host.use_path(path, service)

        if expires:
            host.book.append((path, time() + timeout))
            host.booked_paths.add(path)

        return service.base_path

class HandleFunction(object):
    keyword = 'function'

    def __call__(
        self,
        host, 
        function,
        path = None,
        file_type = None,
        file_name = None,
        content_type = None,
        expires = True,
        timeout = None,
        **keywords
    ):

        if content_type is None:
            content_type = content_types.get(file_type, 'text/plain')
        if file_type is None:
            file_type = file_types.get(content_type, 'txt')

        if path is None:
            path = host.reserve_path(length = 32, file_name = path, file_type = file_type)
        else:
            if not host.path_is_reserved(path):
                raise Exception("Path not reserved")

        if timeout is None:
            timeout = host.timeout

        service = self.Service(
            function = function,
            content_type = content_type,
            host = host,
            path = path,
            expires = expires,
            timeout = timeout,
        )
        host.use_path(path, service)

        if expires:
            host.book.append((path, time() + timeout))
            host.booked_paths.add(path)

        return service.base_path

    class Service(HttpService):

        def __init__(self, host, path, function, content_type, expires, timeout):
            super(HandleFunction.Service, self).__init__()
            self.host = host
            self.path = path
            self.function = function
            self.content_type = content_type
            self.expires = expires
            self.timeout = timeout
            self.last_access = time()

        class Request(HttpRequest):
            def process(self):

                service = self.service
                host = service.host
                path = service.path
                function = service.function
                content_type = service.content_type
                expires = service.expires

                self.setResponseCode(200)
                self.setHeader('Content-type', content_type)
                self.write(function())
                if expires:
                    host.release_path(path)
                self.finish()

class HandleFile(HandleFunction):
    keyword = 'file'
    obviates = []
    def __call__(self, host, file, **keywords):
        if 'expires' in keywords.keys():
            assert keywords['expires'] == True, "Hosted file objects must expire."
        def function():
            return file.read()
        return super(HandleFile, self).__call__(
            host,
            function = function,
            **keywords
        )

class HandleFileName(HandleFunction):
    keyword = 'file_name'
    obviates = []
    def __call__(self, host, file_name, **keywords):
        def function():
            return file(file_name).read()
        return super(HandleFileName, self).__call__(
            host,
            function = function,
            **keywords
        )

class HandleString(HandleFunction):
    keyword = 'string'
    obviates = []
    def __call__(self, host, string, **keywords):
        def function():
            return string
        return super(HandleString, self).__call__(
            host,
            function = function,
            **keywords
        )

class HandleRef(object):
    keyword = 'ref'
    obviates = ['service', 'file', 'file_name', 'string']

    def __init__(self):
        self.refs = {}

    def reserve_path(self, host, ref, **keywords):
        if hash(ref) in self.refs.keys():
            return self.refs[hash(ref)][0]
        else:
            return host.reserve_path(**keywords)

    def __call__(self, host, ref, **keywords):

        if hash(ref) in self.refs.keys():
            if self.refs[hash(ref)][1] == proxy(ref):
                return self.refs[hash(ref)][0]
            else:
                return host(**keywords)
        else:

            def finalize(reference):
                host.release_path(path)
                del self.refs[ref_hash]

            path = host(expires = False, **keywords)
            ref_hash = hash(ref)
            ref_proxy = proxy(ref, finalize)
            del ref
            
            self.refs[ref_hash] = (path, ref_proxy)

            return path

class NoHandlerError(Exception): pass

class AmbiguousHandlerError(Exception): pass

content_types = {
    'js': 'text/javascript',
    'html': 'text/html',
    'css': 'text/css',
    'png': 'image/png',
    'gif': 'image/gif', 'jpg': 'image/jpg',
}

file_types = dict(
    (value, key)
    for key, value in content_types.items()
)

Host = HostService = Service
HostRequest = Service.Request

