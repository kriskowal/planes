
from copy import copy
from planes.sh.application import Application as BaseApplication, run
from protocol import Factory as BaseFactory

class Application(BaseApplication):
    locals = None
    pyrc = None

    def __init__(
            self,
            locals = None,
            globals = None,
            pyrc = None,
            interface = 'localhost',
            *arguments,
            **keywords
        ):
        if locals is not None: self.locals = locals
        if pyrc is not None: self.pyrc = pyrc
        BaseApplication.__init__(self, interface = interface, *arguments, **keywords)

    def Factory(self, *arguments, **keywords):
        factory = BaseFactory(*arguments, **keywords)
        def Init():
            return BaseFactory.Init(
                factory,
                locals = copy(self.locals),
                pyrc = self.pyrc
            )
        factory.Init = Init
        return factory

def run(*arguments, **keywords):
    Application(*arguments, **keywords).run()

PythonHTTPShellApplication = PyshApplication = Application
run_python_http_shell = run_pysh = run

