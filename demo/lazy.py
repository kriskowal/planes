
from planes.lazy import http, host
import planes.lazy

print http.Service
print http.Request
print host.Service
print host.Request

print planes.lazy
print planes.lazy.__path__
print planes.lazy.echo
print planes.lazy.path
print planes.lazy.file
print planes.lazy.auth

from planes.lazy import echo, path, file, auth
from planes.lazy import EchoService, EchoRequest, HostService, HostRequest

print EchoService
print EchoRequest
print HostService
print HostRequest

print planes.lazy.HttpService
print planes.lazy.CommandBoxWidget
print planes.lazy.WidgetFunctionService
from planes.lazy import serve
print serve

