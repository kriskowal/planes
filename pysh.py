
from types import FunctionType
from planes.python.xml.tags import tags, Tag
from planes.python.html_repr import html_repr
from planes.python.module_path import module_path
from planes.lazy import ShellService

use_highlight = True

if use_highlight:
    from planes.python.highlight import highlight

class StdoutRedirector(object):
    """
    Captures stdout from instantiation until close() is called.
    This is not really thread safe! It should be fine as long as
    we stay single threadded.
    """

    def __init__(self):
        import sys
        self.stdout = sys.stdout    # Save old stdout for later
        sys.stdout  = self          # Redirect future calls to write()
        self.data   = ''

    def write(self, str):
        self.data += str

    def close(self):
        import sys
        sys.stdout = self.stdout

    def get(self):
        """
        Returns all of the data buffered up so far and cleans the buffer.
        """
        stuff = self.data
        self.data = ''
        return stuff

class Mode(object):
    """
    A Python interpreter mode.
    """

    prompt = '>>>'

    def __init__(
        self,
        parent = None,
        locals = None,
        globals = None,
        host = None,
        pyrc = None,
        **keywords
    ):
        super(Mode, self).__init__(**keywords)
        # parent is an optional Mode to which slash commands will
        #  be deferred.
        self.parent = parent
        self.locals = locals and locals or {}
        self.globals = globals and globals or self.locals
        self.globals['_'] = None
        self.globals['__'] = []
        self.host = host
        self.locals_stack = []
        self.pyrc = pyrc

    def start(self):
        super(Mode, self).start()
        self.update()
        if self.pyrc is not None:
            self.execute('execfile(%s)' % repr(self.pyrc))

    def command(self, command):
        if command.startswith('/'):
            super(Mode, self).command(command[1:])
        elif command.startswith('exit'):
            self.parent.command('exit')
        elif command.startswith('quit'):
            self.parent.command('quit')
        else:
            self.execute(command)

    def update(self):
        self.depth = None
        if self.globals.has_key('DEPTH'):
            self.depth = int(self.globals['DEPTH'])
        prompt = '>>> '
        if self.globals.has_key('PROMPT'):
            prompt = self.globals['PROMPT']
        if isinstance(prompt, FunctionType):
            prompt = prompt()
        self.prompt = html_repr(prompt, host = self.host, depth = self.depth)

    def execute(self, command):
        kit = self.kit
        tags = kit.tags

        self.update()
    
        # Execute the command
        if use_highlight:
            self.message(tags.p(tags.nobr(self.prompt, ' ', highlight(command))))
        else:
            self.message(tags.p(tags.nobr(self.prompt, command)))

        exception = None
        result = None
        try:

            # Capture stdout so we can exec print commands
            redirector = StdoutRedirector()
            try:
            
                try:
                    result = eval(command, self.globals, self.locals)
                except SyntaxError:
                    exec command in self.locals

            finally:

                # release stdout
                redirector.close()

                # print the standard output
                self.message(html_repr(redirector.get()))

        except Exception, exception:
            pass

        try:

            if result is not None:
                # print the value of the expression
                self.message(html_repr(result, host = self.host, depth = self.depth))
                self.globals['_'] = result
                self.globals['__'].append(result)

        except Exception, exception:
            pass

        if exception is not None:
            # print the exception
            self.message(tags.hr())
            self.message(html_repr(exception))
            self.message(tags.hr())

        self.update()

class Service(ShellService):
    Mode = Mode

PyshService = Service
PyshMode = Mode

