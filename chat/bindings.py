import json

from channels.binding.websockets import WebsocketBinding
from channels.generic.websockets import WebsocketDemultiplexer
from django.contrib.auth.models import User
from django.core import serializers

from .models import Chat


class ChatBinding(WebsocketBinding):
    model = Chat
    stream = "notifications"
    fields = ["text", "room", "user", "datetime", "is_seen"]

    @classmethod
    def group_names(cls, instance):
        group_members = instance.room.getmembers
        group_members.remove(instance.user.username)
        return ["binding.notifications." + member for member in group_members]

    def serialize_data(self, instance):
        data = serializers.serialize('json', [instance],
                                     fields=self.fields,
                                     use_natural_foreign_keys=True,
                                     use_natural_primary_keys=True)
        return json.loads(data)[0]['fields']

    def serialize(self, instance, action):
        instance.user = User.objects.get(username=instance.user.username)
        payload = {
            "action": action,
            "pk": instance.pk,
            "data": self.serialize_data(instance),
            "model": self.model_label,
        }
        return payload

    def has_permission(self, user, action, pk):
        try:
            action in ['update']
        except:
            return False
        return True


class Demultiplexer(WebsocketDemultiplexer):
    http_user = True
    consumers = {
        "notifications": ChatBinding.consumer,
    }

    def connection_groups(self):
        return ["binding.notifications." + self.message.user.username]
