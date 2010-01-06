
from planes.lazy import serve, HostService, ChatService

serve(
    service = HostService(ChatService()),
    port = 8080,
    debug = True,
)

