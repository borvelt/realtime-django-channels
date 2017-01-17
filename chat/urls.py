from channels.routing import route
from .views import (ws_message, ws_add, ws_disconnect)

chat_urls = [
    route("websocket.connect", ws_add),
    route("websocket.receive", ws_message),
    route("websocket.disconnect", ws_disconnect),
]
