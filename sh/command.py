
from glob import glob
from types import GeneratorType
from planes.python.iterkit import all
from session import Mode

class Commands(dict):

    def __init__(self, parent = None):
        self.local = {}
        self.commands = {}
        self.parent = parent

        # implicitly provide all .commands files
        #  with the the decorators in this module
        self.local.update(globals())

    def load(self, *patterns):
        for pattern in patterns:
            for file in glob(pattern):
                execfile(file, self.local)
        self._update()

    def _update(self):

        commands = tuple(
            (name, function)
            for name, function in self.local.items()
            if isinstance(function, Command)
        )
        self.commands.update(commands)
        super(Commands, self).update(commands)

        aliases = dict(
            (alias, function)
            for name, function in self.local.items()
            if isinstance(function, Command)
            for alias in function.aliases
        )
        super(Commands, self).update(aliases)

    def __contains__(self, item):
        if (
            super(Commands, self).__contains__(item) and
            super(Commands, self).__getitem__(item) != None
        ):
            return True
        elif self.parent is not None:
            return item in self.parent
        else:
            return False

    def __getitem__(self, item):
        if (
            super(Commands, self).__contains__(item) and
            super(Commands, self).__getitem__(item) != None
        ):
            return super(Commands, self).__getitem__(item)
        elif self.parent is not None:
            return self.parent.__getitem__(item)
        else:
            return super(Commands, self).__getitem__(item)

class Command(object):

    def __init__(self, function, *arguments, **keywords):

        self.function = function
        self.arguments = arguments
        self.keywords = keywords

        if hasattr(function, '__doc__'):
            self.__doc__ = function.__doc__

        if hasattr(function, 'aliases'):
            self.aliases = function.aliases
        else:
            self.aliases = ()

        if hasattr(function, 'requires'):
            self.requires = function.requires
        else:
            self.requires = ()

    def __call__(self, mode, *arguments, **keywords):

        # TODO: validate arguments and keywords
        # validate requirements against player's rights
        if self.requires and not all(
            require in mode.account.rights
            for require in self.requires
        ):
            mode.message("""
            <p>You do not have permission to run that
            command.</p>
            """)
        else:
            result = self.function(mode, *arguments, **keywords)
            if isinstance(result, GeneratorType):
                mode.push(Mode(result))

def command(*arguments, **keywords):
    def wrap(command):
        return Command(command, arguments, keywords)
    return wrap

def alias(*aliases):
    def wrap(command):
        if not hasattr(command, 'aliases'):
            command.aliases = aliases
        else:
            command.aliases += aliases
        return command
    return wrap

aliases = alias

def require(*requires):
    def wrap(command):
        if not hasattr(command, 'requires'):
            command.requires = requires
        else:
            command.requires += requires
        return command
    return wrap

requires = require
