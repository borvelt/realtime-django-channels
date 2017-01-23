from channels.routing import route

from .consumers import (ws_connect, ws_receive, ws_disconnect, chat_receive)

websocket_routing = [
    route("websocket.connect", ws_connect,
          path=r"^/(?P<channel>[a-zA-Z0-9_]+)$"),
    route("websocket.receive", ws_receive,
          path=r"^/(?P<channel>[a-zA-Z0-9_]+)$"),
    route("websocket.disconnect", ws_disconnect,
          path=r"^/(?P<channel>[a-zA-Z0-9_]+)$"),
]


custom_routing = [
    route("chat.receive", chat_receive, command="^send$"),
]