from channels.auth import channel_session_user
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .exceptions import ClientError
from .models import (Room)
from .utils import catch_client_error


@login_required
def chat_view(request, buddy):
    return render(request, 'chat_view.html', {
        'buddy': buddy,
    })


def load_conversation(request, buddy):
    pass


@catch_client_error
@channel_session_user
def chat_receive(message):
    channel = message.get('channel')
    room = Room.find_by_hash_of(message.user, channel)
    try:
        room.send(message)
    except Exception as e:
        raise ClientError(str(e))
