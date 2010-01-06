#!/usr/bin/env python

from cixar.ish.sh.inoculate import inoculate
from cixar.ish.sh.command import command, aliases, alias

@command()
@aliases('buddy-list', 'buddies')
def who(self):
    """
        <p><b>Usage:</b> <tt>who</tt></p>
        <p>Displays a list of chatters.</p>
    """
    self.message(
        "<p>%s</p>" % "<br/>".join(
            [
                "<b>People Here:</b>",
            ] +
            [
                "%s" % name
                for name in self.chatters.keys()
            ]
        )
    )

@command()
def me(self, *arguments):
    """
        <p><b>Usage:</b> <tt>me <i>does something</i></tt></p>
        <p><b>Example:</b> <tt>me bows</tt></p>
        <p>
            Notifies all other chatters that
            you have performed a given action.
        </p>
    """
    self.emote(" ".join(arguments))

@alias('nick')
@command()
def name(self, new_name):
    """
        <p><b>Usage:</b> <tt>name <i>new-name</i></p>
        <p><b>Example:</b> <tt>name Sam</tt></p>
        <p>Changes your name.</p>
    """
    old_name = self.name
    if old_name == new_name:
        self.message(
            '''
            <p>Your <b>name</b> is <b>already</b>
            <font color="blue">%s</font>.</p>
            ''' % (
                inoculate(new_name)
            )
        )
    else:
        self.set_name(new_name)
        self.message(
            '<p><font color="blue">You are now %s.</font></p>' % (
                inoculate(self.name),
            )
        )
        self.broadcast(
            '<p><font color="blue">%s is now %s.</font></p>' % (
                inoculate(old_name),
                inoculate(self.name),
            )
        )

