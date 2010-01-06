
from sys import modules

class Module(object):

    def _import(self, module_name):
        module = __import__('planes', globals(), {}, (module_name,))
        setattr(self, module_name, getattr(module, module_name))

    def lazy(self, attr):
        return getattr(self, attr)

    def __getattr__(self, attr):

        from planes.python.case import CaseString
        name = CaseString(attr)
        module = None

        for n in range(len(name.parts), 0, -1):
            module_name = CaseString(parts = name.parts[:n]).lower()
            try:
                self._import(module_name)
                module = getattr(self, module_name)
                break
            except AttributeError:
                pass

        if len(name.parts):
            if name.parts[-1] == 'Request':
                return getattr(module, 'Service').Request

        if module is None:
            raise ImportError(attr)

        return getattr(module, attr)

modules[__name__] = Module()

