
from planes.lazy import JsonChatService, ResponseService, serve

serve(ResponseService(JsonChatService()), port = 8080)

