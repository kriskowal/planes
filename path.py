
from planes.response import NotFound, Redirect, Index, tags

class PathService(object):

    paths = None
    service = None
    next_service = None

    def __init__(self, service = None, next_service = None, paths = None, *args, **kws):
        if self.paths is None:
            if paths is None: paths = {}
            self.paths = paths
        if self.service is None:
            if service is None:
                service = IndexService(self)
            self.service = service
        if self.next_service is None or next_service is not None:
            self.next_service = next_service
        super(PathService, self).__init__(*args, **kws)

    def traverse(self, kit):

        # get rid of the initial /
        path = kit.path[1:]

        if not path and self.service:
            next_service = self.service
        else:
            parts = tuple(
                # todo decode
                part for part in 
                path.split('/')
            )
            part = parts[0]
            if part in self.paths:
                next_service = self.paths[part]
                kit.base_path = kit.base_path + '/' + part
                kit.path = path[len(part):]
                self.touch(path)
            else:
                next_service = self.next_service

        return next_service

    def __call__(self, kit, *args, **kws):
        next_service = self.traverse(kit)
        if not next_service:
            return NotFound(kit.full_path)
        return next_service(kit, *args, **kws)

    def touch(self, path):
        pass

    def decorate(self, url):
        def decorator(service):
            self.paths[url] = service
            return service
        return decorator

def IndexService(service):
    def wrapper(kit):
        if kit.path.endswith('/'):
            return Index(kit.full_path, service.paths)
        else:
            return Redirect(kit.full_path + '/')
    return wrapper

