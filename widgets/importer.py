
from sys import modules

class Module(object):

    def _import(self, module_name):
        module =  __import__('planes.widgets', globals(), {}, (module_name,))
        setattr(self, module_name, getattr(module, module_name))

    def __getattr__(self, attr):
        try:

            from planes.python.case import CaseString
            name = CaseString(attr)
            module_name = name.lower()
            self._import(module_name)
            module = getattr(self, module_name)

            if name.is_title():
                return getattr(module, attr)
            else:
                return getattr(self, attr)

        except:
            from traceback import print_exc
            print_exc()
            raise

modules['planes.widgets.importer'] = Module()

