from django.conf.urls import url

from .views import (load_conversation, chat_view, load_notifications)

urlpatterns = [
    url(r'^$', chat_view),
    url(r'^/notifications$', load_notifications),
    url(r'^/(?P<buddy>[\w.@+-]+)$', chat_view),
    url(r'^/(?P<buddy>[\w.@+-]+)/retrieve$', load_conversation),
]
