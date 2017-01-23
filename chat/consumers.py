from channels import Channel
from channels.generic.websockets import (JsonWebsocketConsumer)
from django.contrib.auth.models import User
import json
from .models import (Room)


class Consumer(JsonWebsocketConsumer):
    channel_session_user = True
    http_user = True

    def connect(self, content, **kwargs):
        reply = {"accept": False}
        room = None
        try:
            User.objects.filter(username=kwargs['channel']).get()
        except:
            self.message.reply_channel.send(reply)
            return
        try:
            room = Room.find_by_hash_of(kwargs['channel'], self.message.user)
            reply = {"accept": True}
        except:
            try:
                room = Room(members=[kwargs['channel'], self.message.user.username])
                room.save()
                reply = {"accept": True}
            except:
                pass
        try:
            assert room
            self.message.reply_channel.send(reply)
            room.channel.add(self.message.reply_channel)
        except:
            self.message.reply_channel.send(reply)

    def receive(self, content, **kwargs):
        payload = json.loads(self.message['text'])
        payload['channel'] = kwargs['channel']
        payload['reply_channel'] = self.message.content['reply_channel']
        Channel("chat.receive").send(payload)

    def disconnect(self, message, **kwargs):
        try:
            room = Room.find_by_hash_of(self.message.user, kwargs['channel'])
            room.channel.discard(self.message.reply_channel)
        except:
            pass
