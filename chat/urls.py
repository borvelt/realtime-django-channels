from django.conf.urls import url

from .views import (load_conversation, chat_view)

urlpatterns = [
    url(r'^/(?P<buddy>[\w.@+-]+)$', chat_view),
    url(r'^/(?P<buddy>[\w.@+-]+)/retrieve$', load_conversation),
]
