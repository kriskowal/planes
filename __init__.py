"""\
A framework for web services.

Provides building blocks for web services built on top of the Twisted Web
Application Framework (Python module twisted).

Basics:
    service
    application

Services:
    http
    path
    file
    object and function
    host
    adhoc
    auth
    auth_shadow
    auth_shadow_self

Protocols:
    sh
    pysh
    chat

Daemons:
    (these are shebang unix commands, not modules)
    pyshd <file>
    chatd

Small, general modules organized by shape:
    protocols (Factory, Channel, Request)
    services (Service, Request)
    modes (Mode)
    commands (command functions)
    content (static web content)

"""
__doc_svn_version__ = 34

__all__ = (
)

