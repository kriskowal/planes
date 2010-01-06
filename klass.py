
from planes.lazy import PathService, BaseService

def bind(function, self):
    def wrapper(*args, **kws):
        return function(self, *args, **kws)
    return wrapper

class KlassService(PathService):
    def __init__(self, *args, **kws):
        super(KlassService, self).__init__(*args, **kws)
        for key, value in self.__class__.__dict__.items():
            if not key.startswith('_'):
                self.paths[key] = bind(value, self)

Service = KlassService

