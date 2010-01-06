# not yet used.  should be in host.py

from urllib import unquote

class FunctionService(object):

    def __init__(self, service):
        self.service = service

    def __call__(self, kit, *args, **kws):
        service = self.service
        kit.service = service

        args = list(args)

        args.extend(
            unquote(arg)
            for arg in kit.path[1:].split('/')
            if arg
        )
        kws.update(
            (key, values[0]) 
            for key, values in kit.keywords
        )

        return service(kit, *args, **kws)

Service = FunctionService

