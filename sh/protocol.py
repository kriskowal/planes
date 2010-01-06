"""

This module provides a Twisted Web Application Framework protcol
for producing web based shell-like user interfaces.

This module provides the following interfaces:

    HTTPShellFactory = Factory
    HTTPShellSession = Session
    HTTPShellMode = Mode
    HTTPShellSessionRequest = SessionRequest
    HTTPShellSessionService = SessionService 
Factory(
    InitialMode,
    reactor = default_reactor
)

The programmer must provide an initial shell mode, Init.

The factory requires the handle of a reactor that will
always be running when it is running so that it can
schedule session bookkeeping.  This includes but is
conceptually not limited to expiration of obsolete
sessions.

"""

import os
import random
import string
from time import time
from traceback import print_exc

#+https://planes.com/svns/python
# planes's python package
from planes.python.xml.tags import tags
from planes.python.html_repr import html_repr
from planes.python.threadtools import synchronized_method
from planes.python.module_path import module_path
from planes.python.session import Session as SessionBase, Mode as ModeBase

from planes.service import ServiceFactory
from planes.path import PathRequest, PathService
from planes.http import HttpRequest, HttpService
from planes.file import FileRequest, FileService
from inoculate import inoculate

# causes each session request to wait a number of
#  seconds before responding.  use this to test
#  how the client reacts to a laggy server.
debug_lag = 0

class SessionEndedError(AttributeError): pass

class ClientRequest(HttpRequest):

    splash_title = ''
    argument = ''
    js_files = (
        '.sh/domSupplement.js',
        '.sh/messages.js',
        '.sh/overlays.js',
        '.sh/poll.js',
    )
    css_files = (
        '.sh/@.css',
    )
    log = []

    @property
    def html(self):
        factory = self.channel.factory
        return """\
            <html>
                <head>
                    <title>&nbsp;</title>
                    <style type="text/css" media="all">
                        %(stylesheets)s
                    </style>
                </head>
                <body id="buffer">
                    <table height="98%%" width="100%%">
                        <tr>
                            <td align="center" width="50%%"></td>
                            <td align="center" id="title">%(splash_title)s</td>
                            <td align="center" width="50%%"></td>
                        </tr>
                    </table>
                    <div id="log" style="opacity: .5">%(log)s</div>
                    <span id="bufferEnd"/>
                    <div id="input">
                        <table width="100%%" id="inputTable">
                            <tr>
                                <td><nobr id="prompt">:</nobr></td>
                                <td width="100%%"><input type="textbox" id="command"/></td>
                            </tr>
                        </table>
                    </div>
                    %(scripts)s
                    <script>window.ish(%(argument)s, %(send_commands_immediately)s, %(session_url)s);</script>
                </body>
            </html>
        """ % {
            'splash_title': self.splash_title or '&nbsp;',
            'scripts': "".join(
                """<script src=%s></script>""" % repr(js_file)
                for js_file in self.js_files
            ),
            'stylesheets': "".join(
                """@import url(%s);\n""" % css_file
                for css_file in self.css_files
            ),
            'log': "".join(
                '<p>%s</p>' % entry
                for entry in self.log
            ),
            'argument': repr(self.argument),
            'send_commands_immediately': factory.manageGreedySessions and '0' or '1',
            'session_url': repr(factory.session_url),
        }

class ClientService(HttpService, object):
    Request = ClientRequest

class SessionRequest(HttpRequest):

    def process(self):
        """Process HTTP Requests for session mode XML snippets.
        The client uses discrete and frequent HttpRequests to
        aquire new messages and update their prompt and form."""

        if debug_lag:
            print 'begin lag'
            from time import sleep
            sleep(debug_lag)
            print 'end lag'

        factory = self.channel.factory

        # get a session
        # the request's service is a SessionService
        session_service = self.service
        try:
            # if a session has been specified, attempt to aquire it
            if self.args.has_key('session'):
                key = self.args['session'][0]
                if key != '':
                    session = session_service[key]
                    if not session.modes:
                        session = session_service.generateSession()
                else:
                    session = session_service.generateSession()
            else:
                session = session_service.generateSession()
        # if the request specified a session which has expired or
        #  or did not exist in the first place:
        except KeyError:
            # create a fresh session and notify the user that
            #  their session has been recreated.  Use a priority
            #  message so that it gets sent before the welcome message.
            session = session_service.generateSession()
            session.priorityMessage(
                'The <b>server</b> has begun a new <b>session</b> with you.'
            )

        # record that this is the last time that the session
        #  was accessed, so as to avoid expiration until the next
        #  period of the factory's timeout.
        lastAccess = time()

        # if the client polls too frequently, give them a
        #  service temporarily unavailable error
        if (
            False and
            # todo: fix this and turn it back on
            session.lastAccess is not None and
            lastAccess - session.lastAccess < 
             factory.sessionPollInterval
        ):
            self.setResponseCode(503) # Service Unavailable
            self.finish()
            print "Greedy session: %s, %s" % (session.key, self.getHost())
            del session_service[session.key]
            return

        session.lastAccess = lastAccess

        try:
            if self.args.has_key('command'):
                
                # execute any commands that were sent in the URL or POST body.
                commands = self.args['command']
                for command in commands:
                    session.command(command)

            # run the optional user defined HttpRequest process handler
            session.tick()
            session.process(self)

        except SessionEndedError:
            session = session_service.generateSession()

        # send any queued cookies
        for key, value in session.cookies:
            self.addCookie(key, value)
        del session.cookies[:]
        
        # send an XML response including all new messages and updates
        #  for the client mode, including the current session key
        #  for future reference.
        self.setResponseCode(200) # OK
        self.setHeader('Content-type', 'text/xml')

        envelope = tags.envelope(
            tags.session(session.key),
            tags.pollInterval(factory.session_service.pollInterval),
            tags.prompt(session.prompt),
            tags.silent(session.silent and 'yes' or 'no'),
            tags.title(session.title),
            tags.messages(
                tags.message(message)
                for message in session.priorityMessages + session.messages
            ),
            tags.overlays(
                tags.overlay(overlay)
                for name, overlay in session.overlays.items()
            ),
        )
        # this code helps observe that XML HTTP Request responses
        # are limited to 8KB in Firefox.
        #    if len(envelope.xml) > 400:
        #        print len(envelope.xml)
        # eventually, we'll have to trim messages down to discrete
        #  patches to send to the user document
        xml = envelope.xml
        if len(xml) > 8 * 1024:
            print "Message longer than 8KB (%sKB)." % (len(xml) / 1024)
        envelope.writexml(self)

        # remove the messages that have been sent from their queues
        del session.messages[:]
        del session.priorityMessages[:]
        session.overlays.clear()

        self.finish()

class SessionService(HttpService, dict):

    def __repr__(self): return object.__repr__(self)

    bookKeepingInterval = 5.0 # seconds
    pollInterval = 1.0 # seconds
    timeout = 10 # seconds
    Request = SessionRequest

    # an alphabet for generating random session keys.
    alphabet = string.ascii_letters + string.digits

    # todo: accept alternate base_url's for the session service
    def __init__(self, factory, **keywords):
        super(SessionService, self).__init__(**keywords)
        self.factory = factory

        def bookKeepingLoop():
            self.bookKeeping()
            self.factory.reactor.callLater(
                self.bookKeepingInterval,
                bookKeepingLoop
            )
        bookKeepingLoop()

    # produces a random key given a random number generator
    def randomKey(self, randomGenerator):
        return "".join(
            randomGenerator.choice(self.alphabet)
            for n in range(0, 32)
        )

    randomGenerator = random.WichmannHill()

    @synchronized_method
    def generateKey(self):
        session = object()
        key = self.randomKey(self.randomGenerator)
        while key in self:
            key = self.randomKey(self.randomGenerator)
        # store the stub session so we know not
        #  to use it again
        self[key] = None
        return key

    def generateSession(self):
        """builds and returns a new Session."""
        key = self.generateKey()
        session = self.factory.Session(key, self, self.factory.Init)
        self[key] = session
        print "Session created: %s" % key
        return session

    def bookKeeping(self):
        """deletes all sessions that have been idle for longer than
        the Factory.session_service.timeout"""

        now = time()
        items = self.items()
        for key, session in items:
            # destroy placeholder sessions
            if session is None:
                del self[key]
            # destroy sessions that have not voluntarily
            #  removed themselves from the service upon exiting
            elif session.lastAccess + self.factory.session_service.timeout < now:
                # sessions should voluntarily remove themselves
                # from the service if there are no more modes on their stack
                assert session.modes
                try:
                    print "Session expired: %s" % key
                    self[key].exit()
                    # onExit takes care of removal
                except:
                    print (
                        "Exception caught while forcing " +
                        "a session to exit"
                    )
                    print_exc()
                assert key not in self

class Session(SessionBase):

    def __init__(self, key, session_service, Init):
        """Constructs a new Session, with a unique session key, so that
        multiple HTTPRequests can find their corresponding session object.

        Assures that the key has enough entropy to be difficult to acquire
        by brute force.  Initializes properties of client, and begins
        running the service's welcome prompt mode."""

        SessionBase.__init__(self)
        self.key = key
        self.session_service = session_service

        # the current text to display with the command line
        self.prompt = ":"
        # whether the command line is 'silent', not openly displaying the
        #  command that the user enters, particularly if the command
        #  is a password.
        self.silent = False
        # messages that are ready for the client to enqueue in their
        #  message buffer
        self.messages = []
        # messages that the client should enqueue before any normal messages,
        #  such as exceptions
        self.priorityMessages = []
        # updates for the client document
        self.overlays = {}
        # cookies to set
        self.cookies = []
        # the client's current widow title
        self.title = ""

        # initialize timer
        self.lastAccess = None

        # push the initial mode
        self.push(Init())

    # interface provisions for user interface modes
    def message(self, message):
        self.messages.append(message)
    def cookie(self, key, value):
        self.cookies.append((key, value))
    def priorityMessage(self, message):
        self.priorityMessages.append(message)
    def overlay(self, name, overlay):
        self.overlays[name] = overlay
    def setPrompt(self, prompt):
        self.prompt = prompt
    def setSilent(self, silent = True):
        self.silent = silent
    def setTitle(self, title):
        self.title = title

    def onExit(self):
        # voluntarily remove self from the session service so
        #  we don't have to be harvested by the book keeper
        print "Session ended: %s" % self.key
        session_service = self.session_service
        del session_service[self.key]

    def __getattr__(self, key):
        try:
            return super(Session, self).__getattr__(key)
        except AttributeError, x:
            raise SessionEndedError(
                'Cannot access attribute %s because the session %s has ended' % (
                    repr(key) ,
                    repr(self.key),
                )
            )

class Mode(ModeBase):

    def __init__(self):
        self.title = ''
        self.silent = False
        self.prompt = ':'

    #def tick(self):
    #    super(Mode, self).tick()
        # TODO move this over to the Mage/Tale repository to reactivate it there
        #if hasattr(self, 'account') and self.account is not None:
        #    self.account.overlay_map()
        #    self.account.overlay_hud()

    # this function gives Modes an opportunity to handle incoming
    #  HTTPRequsts to do things like initialize values that
    #  are only accessible in cookies
    def process(self, http_request):
        pass

    def start(self):
        super(Mode, self).start()
        self.session.setPrompt(self.prompt)
        self.session.setSilent(self.silent)
        self.session.setTitle(self.title)

    def resume(self):
        super(Mode, self).resume()
        self.session.setPrompt(self.prompt)
        self.session.setSilent(self.silent)
        self.session.setTitle(self.title)

    def command(self, command):

        # todo: integrate swil parsing matter

        # a command parsing stand in, for now
        # TODO replace this parser with something worthy
        pos = command.find(" ")
        if pos != -1:
            args = command[pos+1:].split(" ")
            command = command[:pos]
        else:
            args = []

        # command dispatch
        if command in self.commands:
            function = self.commands[command]
            try:
                function(self, *args)
            except TypeError, exception:
                self.message(
                    """
                        <p>That is not the <b>proper usage</b>
                        for the <tt>%s</tt> command.</p>
                    """ % inoculate(repr(command))
                )
                print_exc()
            except Exception, exception:
                if hasattr(self, 'message'):
                    self.message(tags.hr().xml)
                    self.message(html_repr(exception))
                    self.message(tags.hr().xml)
        else:
            self.message("<p><b>Huh?</b>  <tt>%s</tt> isn't a command.</p>" % repr(inoculate(command)))

class Factory(ServiceFactory):
    """Provides HTTP protocol services, by creating HTTP Channels
    for the MAGE protocol.
    
    Also manages sessions which persist
    between HTTP requests, and provides a reference to a common service
    mode for all all requests."""

    # whether to log individual HTTP Requests
    log_requests = False

    manageGreedySessions = False
    session_url = 'session'

    Session = Session
    SessionService = SessionService
    SessionRequest = SessionRequest
    ClientRequest = ClientRequest
    FileService = FileService
    FileRequest = FileRequest

    def __init__(
        self, 
        Init = None,
        Session = None,
        reactor = None,
    ):
        """Initializes a Factory for serving a service
        that starts with a given initial mode.
        Passes any and all other arguments to
        the HTTPFactory initilizer."""

        if Init is not None:
            self.Init = Init
        if Session is not None:
            self.Session = Session
        if reactor is None:
            from twisted.internet import reactor
        self.reactor = reactor

        # path_service
        #  v  /session -> session_service
        # file_service
        #  v  
        # client_service

        self.client_service = ClientService() # hosts the client HTML page

        self.file_service = self.FileService() # hosts static content
        self.file_service.next_service = self.client_service # all file service misses load the client page

        # populate file service file mapping
        for name in os.listdir(module_path(__file__, 'content')):
            self.file_service.contents['.sh/' + name] = module_path(
                __file__,
                'content',
                name
            )

        self.session_service = self.SessionService(self) # hosts the polling XML request page

        self.path_service = PathService()
        self.path_service[self.session_url] = self.session_service # session service is hosted on /session
        self.path_service.next_service = self.file_service
        self.path_service.service = self.client_service

        self.service = self.path_service

    def log(self, request):
        if self.log_requests:
            SiteFactory.log(self, request)

# more specific names for imports
HTTPShellClientRequest = ClientRequest
HTTPShellSessionRequest = SessionRequest
HTTPShellSessionService = SessionService
HTTPShellSession = Session
HTTPShellMode = Mode
HTTPShellFactory = Factory

