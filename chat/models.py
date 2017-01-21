import json

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Room(models.Model):
    name = models.CharField(_('Name'), max_length=64, unique=True, null=False, blank=False)
    members = models.CharField(_('Members'), max_length=500, null=False, blank=False)

    def setmembers(self, x):
        self.foo = json.dumps(x)

    def getmembers(self):
        return json.loads(self.foo)


class Chat(models.Model):
    text = models.CharField(_('Text'), max_length=1000, null=False, blank=False)
    datetime = models.DateTimeField(_('Chat Date Time'))
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    room = models.ForeignKey(Room)
