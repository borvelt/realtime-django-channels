import json
import ast
from datetime import datetime

from channels import Group
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .utils import sha256_of


class Room(models.Model):
    name = models.CharField(_('Name'), max_length=64, unique=True, null=False, blank=False)
    members = models.CharField(_('Members'), max_length=500, null=False, blank=False)

    def setmembers(self, x):
        self.members = json.dumps(x)

    @property
    def getmembers(self):
        return ast.literal_eval(self.members)

    def natural_key(self):
        return self.name

    def send(self, message):
        chat = Chat(text=message['text'],
                    room=self,
                    datetime=datetime.now(),
                    user=message.user,
                    is_seen=True)
        chat.save()
        self.channel.send({
            "text": json.dumps({
                "text": chat.text,
                "user": chat.user.username,
                "datetime": str(chat.datetime)
            })
        })

    def save(self, *args, **kwargs):
        self.name = sha256_of(self.members)
        super(Room, self).save(*args, **kwargs)

    @staticmethod
    def find_by_hash_of(*args):
        name = sha256_of(args)
        try:
            return Room.objects.get(name=name)
        except:
            raise Room.DoesNotExist

    @property
    def channel(self):
        return Group("room-%s" % self.id)


class Chat(models.Model):
    text = models.CharField(_('Text'), max_length=1000, null=False, blank=False)
    datetime = models.DateTimeField(_('Chat Date Time'))
    user = models.ForeignKey(User)
    room = models.ForeignKey(Room)
    is_seen = models.BooleanField(_('Is Message Seen'), default=False)
