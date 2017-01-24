from channels import (route, route_class)

from .bindings import Demultiplexer
from .consumers import Consumer
from .views import chat_receive

websocket_routing = [
    route_class(Demultiplexer, path=r"^/bindings$"),
    Consumer.as_route(path=r"^/(?P<channel>[a-zA-Z0-9_]+)$"),
]

custom_routing = [
    route("chat.receive", chat_receive),
]
