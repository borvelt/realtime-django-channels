from channels.routing import route
from django.conf.urls import url

from .chat_client import basic_view
from .views import (ws_message, ws_add, ws_disconnect)

chat_urls = [
    route("websocket.connect", ws_add, path=r"^/(?P<channel>[a-zA-Z0-9_]+)$"),
    route("websocket.receive", ws_message, path=r"^/(?P<channel>[a-zA-Z0-9_]+)$"),
    route("websocket.disconnect", ws_disconnect, path=r"^/(?P<channel>[a-zA-Z0-9_]+)$"),
]

urlpatterns = [
    url(r'^$', basic_view),
]
