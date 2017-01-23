from django.conf.urls import url

from .views import chat_view

urlpatterns = [
    url(r'^/(?P<buddy>.+)$', chat_view),
]
