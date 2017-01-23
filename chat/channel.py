import json
from datetime import datetime

from channels import Group
from channels.auth import channel_session_user, channel_session_user_from_http
from django.contrib.auth.models import User

from .models import (Room, Chat)
from .utils import recognize_room_name


@channel_session_user_from_http
def ws_add(message, channel):
    reply = {"accept": False}
    room_name = recognize_room_name(channel, message.user)
    try:
        User.objects.filter(username=channel).get()
    except:
        message.reply_channel.send(reply)
        return
    try:
        room = Room.objects.get(name=room_name)
        reply = {"accept": True}
    except:
        try:
            room = Room(name=room_name, members=[channel, message.user.username])
            room.save()
            reply = {"accept": True}
        except:
            room = None
    try:
        assert len(room.name)
        message.reply_channel.send(reply)
        Group("room-%s" % room.name).add(message.reply_channel)
    except:
        message.reply_channel.send(reply)


@channel_session_user
def ws_message(message, channel):
    room_name = recognize_room_name(channel, message.user)
    try:
        User.objects.filter(username=channel).get()
    except:
        ws_disconnect(message, channel)
        return
    try:
        room = Room.objects.get(name=room_name)
        try:
            chat = Chat(text=message['text'], room=room, datetime=datetime.now(), user=message.user)
            chat.save()
            Group("room-%s" % room.name).send({
                "text": json.dumps({
                    "body": chat.text,
                    "user": chat.user.username,
                    "datetime": str(chat.datetime)
                }),
            })
        except Exception as e:
            print(str(e))
    except:
        ws_disconnect(message, channel)


@channel_session_user
def ws_disconnect(message, channel):
    Group("room-%s" % recognize_room_name(channel, message.user)).discard(message.reply_channel)
