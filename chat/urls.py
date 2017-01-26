from django.conf.urls import url

from .views import (load_conversation,
                    room_view,
                    load_notifications,
                    chat_list)

urlpatterns = [
    url(r'^$', chat_list, name='users_list'),
    url(r'^/notifications$', load_notifications, name='notifications'),
    url(r'^/(?P<buddy>[\w.@+-]+)$', room_view, name='room_view'),
    url(r'^/(?P<buddy>[\w.@+-]+)/retrieve$', load_conversation, name='load_conversation'),
]
