
from types import FunctionType
from planes.python.xml.tags import tags, Tag
from planes.python.html_repr import html_repr
from planes.python.module_path import module_path
from planes.sh.command import Commands
from session import Mode

use_highlight = True

if use_highlight:
    from planes.python.highlight import highlight

class Init(Mode):
    """
    A Python interpreter mode.
    """

    commands = Commands()

    def __init__(
        self,
        parent = None,
        locals = None,
        globals = None,
        host = None,
        pyrc = None,
    ):
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

        self.message("""
            <p>Entering <b>Python</b> mode.</p>
        """)

        if self.pyrc is not None:
            self.execute('execfile(%s)' % repr(self.pyrc))

        if self.parent is not None: self.message("""
            <p><i>
            Prefix your command with '<tt>/</tt>' to execute a regular command.
            </i></p>
        """)

    def stop(self):
        self.message("<p>Exiting <b>Python</b> mode.</p>");
        super(Mode, self).stop()
    
    def command(self, command):
        if command.startswith('/'):
            super(Init, self).command(command[1:])
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
        self.session.prompt = html_repr(prompt, host = self.host, depth = self.depth).xml

    def execute(self, command):

        self.update()
    
        # Execute the command
        if use_highlight:
            self.message('<p><nobr>%s %s</nobr></p>' % (self.session.prompt, highlight(command)))
        else:
            self.message(tags.p(tags.nobr(self.session.prompt, command)))

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
                self.message(html_repr(redirector.get()).xml)

        except Exception, exception:
            pass

        try:

            if result is not None:
                # print the value of the expression
                self.message(html_repr(result, host = self.host, depth = self.depth).xml)
                self.globals['_'] = result
                self.globals['__'].append(result)

        except Exception, exception:
            pass

        if exception is not None:
            # print the exception
            self.message(tags.hr().xml)
            self.message(html_repr(exception).xml)
            self.message(tags.hr().xml)

        self.update()

Init.commands.load(
    module_path(__file__, 'commands.py'),
    module_path(__file__, '..', 'sh', 'general_commands.py'),
)

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

