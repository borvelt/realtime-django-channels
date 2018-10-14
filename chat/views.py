import json

from channels.auth import channel_session_user
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import render

from .exceptions import ClientError
from .models import (Room, Chat)
from .utils import catch_client_error


@login_required
def room_view(request, buddy):
    room_name = None
    try:
        room = Room.find_by_hash_of(request.user, buddy)
        room_name = room.name
    except Room.DoesNotExist:
        pass
    return render(request, 'chat.html', {
        'buddy': buddy,
        'room': room_name,
        'username': request.user.username
    })


@login_required
def load_conversation(request, buddy):
    try:
        assert request.is_ajax(), "Ajax Request Required."
        assert request.user.is_authenticated(), "Anonymous User Not Allowed."
        room = Room.find_by_hash_of(request.user, buddy)
        all_relative_chats = Chat.objects.filter(room=room)
        all_relative_chats.exclude(user=request.user.pk).update(is_seen=True)
        chats = serializers.serialize('json',
                                      all_relative_chats,
                                      use_natural_foreign_keys=True,
                                      use_natural_primary_keys=True)
        room = serializers.serialize('json', [room])
        chats_result = json.loads(chats)
        chats_room = json.loads(room)
        return JsonResponse({'chats': chats_result, 'room': chats_room})
    except Exception as e:
        print(str(e))
        return JsonResponse({"error": str(e)}, status=500)


@login_required
def load_notifications(request):
    try:
        assert request.is_ajax(), "Ajax Request Required."
        assert request.user.is_authenticated(), "Anonymous User Not Allowed."
        founded_chats = Chat.objects.filter(is_seen=False) \
            .exclude(user=request.user.pk) \
            .order_by('-datetime')
        founded_chats = [chat for chat in founded_chats if request.user.username in chat.room.getmembers]
        chats = serializers.serialize('json',
                                      founded_chats,
                                      use_natural_foreign_keys=True,
                                      use_natural_primary_keys=True)
        chats_result = json.loads(chats)
        return JsonResponse({'notifications': chats_result})
    except Exception as e:
        print(str(e))
        return JsonResponse({"error": str(e)}, status=500)


@login_required
def chat_list(request):
    users_list = User.objects.exclude(username=request.user.username)
    serialized_users_list = serializers.serialize('json',
                                                  users_list,
                                                  fields=['username', 'pk'])
    serialized_users = json.loads(serialized_users_list)
    return render(request, 'chat_list.html', {
        'users_list': serialized_users,
        'username': request.user.username
    })


@catch_client_error
@channel_session_user
def chat_receive(message):
    channel = message.get('channel')
    room = Room.find_by_hash_of(message.user, channel)
    try:
        assert len(message.get('text')), "MESSAGE_EMPTY"
        room.send(message)
    except Exception as e:
        raise ClientError(str(e))
