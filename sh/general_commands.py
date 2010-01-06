#!/usr/bin/env python

from planes.python.iterkit import all

@command()
@aliases('x', 'quit', 'q')
def exit(self):
    """
        <p>Usage: <tt>exit</tt></p>
        <p>Exits the current mode.  From play mode, exits the game; from chat mode, returns to play mode.</p>
    """
    self.pop()

def commands(self):
    """
        <p>Usage: <tt>commands</tt></p>
        <p>Displays information about available commands.</p>
    """
    # This command is now working with the quadtree.

    self.message("""
        <h1>Commands:</h1>
        <ul>%s</ul>
        <p><i>(?) denotes commands for which help is available.</i></p>
        %s
    """ % (
        "".join(
            """<li>%s%s%s</li>""" % (
                name,
                (
                    command.aliases and 
                    (
                        ", %s" %
                        ", ".join(
                            "<b>%s</b>" % alias
                            for alias in command.aliases
                        )
                    ) or ""
                ),
                (
                    command.__doc__ and " (?)" or ""
                ),
            )
            for name, command in sorted(self.commands.commands.items())
            if not command.requires or all(
                require in self.account.rights
                for require in command.requires
            )
        ),
        hasattr(self, 'help') and self.help or ''
    ))

@command()
@alias('h', '?')
def help(self, *args):
    """
        <p>Usage: <tt>help</tt> or <tt>help <i>command</i></tt></p>
        <p>Displays information about available commands.</p>
    """
    # This command is now working with the quadtree.

    if len(args) == 0:
        commands(self)
    else:
            
        for command in args:
            if command not in self.commands.keys():
                self.message("""
                    <p><tt>%s</tt> is not a command.</p>
                """ % (command))
            elif self.commands[command].__doc__:
                self.message("""
                    <h1>Help on <tt>%s</tt></h1>
                    %s
                """ % (command, self.commands[command].__doc__))
            else:
                self.message("""
                    <p>No help available on <tt>%s</tt></p>
                """ % (command))

