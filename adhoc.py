"""provides adhoc hosting middle-ware."""

import random
import string
from time import time
from planes.lazy import PathService

class AdhocDict(dict):

    alphabet = string.ascii_letters + string.digits
    length = 64

    def randomkey(self, length = None, alphabet = None):
        if length is None: length = self.length
        if alphabet is None: alphabet = self.alphabet
        return "".join(
            random.choice(alphabet)
            for n in range(0, length)
        )

    def getkey(self, length = None, alphabet = None):
        while True:
            key = self.randomkey(length = length, alphabet = alphabet)
            if key not in self:
                break
        return key

    def setvalue(self, value):
        key = self.getkey()
        self[key] = value
        return key

class AdhocService(PathService):

    timeout = 10
    path_length = 6
    keeping_book = False
    book_keeping_interval = 1

    def __init__(self, ref_path = None, *args, **kws):
        self.ref_path = ref_path
        super(AdhocService, self).__init__(
            paths = AdhocDict(),
            *args, **kws
        )

    def serve(
        self,
        kit,
        service,
        expires = None,
        timeout = None,
        path = None,
        length = None,
        alphabet = None,
    ):

        if expires is None:
            expires = False
        if timeout is None:
            timeout = self.timeout

        if path is None:
            path = self.paths.getkey(
                length = length,
                alphabet = None,
                #prefix = None,
                #suffix = None,
            )

        self.paths[path] = service

        if expires:
            self.keep_book(kit)
            self.book.append((path, time(), timeout))
            self.booked_paths.add(path)

        if self.ref_path is not None:
            path = self.ref_path + '/' + path
        return path

    def touch(self, path):
        print 'touch', path
        if path in self.booked_paths:

            now = time()
            service = self.paths[path]

            if hasattr(service, 'last_access'):
                service.last_access = now
            else:
                self.book = [
                    (book_path, last_access, timeout)
                    for book_path, last_access, timeout in self.book
                    if book_path != path
                ]

            self.book.append((path, now, timeout))

    def release_path(self, path):
        del self.paths[path]
        del self.book[path]
        self.booked_paths.discard(path)
        self.booked_paths

    def keep_book(self, kit):
        if self.keeping_book:
            return

        self.book = []
        self.booked_paths = set()
        reactor = kit.reactor

        # arrange for old content to expire
        self.book = []
        self.booked_paths = set()
        def book_keeping_loop():
            self.book_keeping()
            reactor.callLater(
                self.book_keeping_interval,
                book_keeping_loop
            )
        book_keeping_loop()

    def book_keeping(self):
        now = time()
        while self.book:
            path, last_access, timeout = self.book[0]
            expiration = last_access + timeout
            if expiration < now:
                if path in self.paths:
                    # recheck the expiration time in case the
                    # service has been last_access
                    service = self.paths[path]
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

def AdhocKitService(service = None, adhoc = None, path = None):

    if service is None:
        def curry(service):
            return AdhocKitService(
                service = service,
                adhoc = adhoc,
                path = path
            )
        return curry

    def wrapper(kit, *args, **kws):
        def serve(*args, **kws):
            return adhoc.serve(kit, *args, **kws)
        kit.serve = serve
        return service(kit, *args, **kws)

    if adhoc is None:
        adhoc = AdhocService(service = wrapper, next_service = wrapper)
        return adhoc
    else:
        return wrapper

Dict = AdhocDict
Service = AdhocService
KitService = AdhocKitService

