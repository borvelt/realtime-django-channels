from .consumers import Consumer
from .views import chat_receive
from channels import route

websocket_routing = [
    Consumer.as_route(path=r"^/(?P<channel>[a-zA-Z0-9_]+)$"),
]

custom_routing = [
    route("chat.receive", chat_receive),
]
