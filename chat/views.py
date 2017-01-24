import json

from channels.auth import channel_session_user
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import render

from .exceptions import ClientError
from .models import (Room, Chat)
from .utils import catch_client_error


@login_required
def chat_view(request, buddy):
    return render(request, 'chat_view.html', {
        'buddy': buddy,
    })


def load_conversation(request, buddy):
    try:
        # assert request.is_ajax(),  "Ajax request required"
        assert request.user.is_authenticated()
        room = Room.find_by_hash_of(request.user, buddy)
        chats = serializers.serialize('json',
                                      Chat.objects.filter(room=room).all(),
                                      use_natural_foreign_keys=True,
                                      use_natural_primary_keys=True)
        room = serializers.serialize('json', [room])
        chats_result = json.loads(chats)
        chats_room = json.loads(room)
        return JsonResponse({"chats": chats_result, "room": chats_room})
    except Exception as e:
        print(str(e))
        return JsonResponse({"error": str(e)}, status=500)


@catch_client_error
@channel_session_user
def chat_receive(message):
    channel = message.get('channel')
    room = Room.find_by_hash_of(message.user, channel)
    try:
        room.send(message)
    except Exception as e:
        raise ClientError(str(e))
