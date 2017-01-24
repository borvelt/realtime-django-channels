from channels.binding.websockets import WebsocketBinding
from channels.generic.websockets import WebsocketDemultiplexer

from .models import Chat


class ChatBinding(WebsocketBinding):
    model = Chat
    stream = "notifications"
    fields = ["text", "room", "user"]

    @classmethod
    def group_names(cls, instance):
        group_members = instance.room.getmembers
        group_members.remove(instance.user.username)
        return ["binding.notifications." + member for member in group_members]

    def has_permission(self, user, action, pk):
        print('user', user)
        print('action', action)
        print('pk', pk)
        return False


class Demultiplexer(WebsocketDemultiplexer):
    http_user = True
    consumers = {
        "notifications": ChatBinding.consumer,
    }

    def connection_groups(self):
        return ["binding.notifications." + self.message.user.username]
