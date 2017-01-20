from channels import Group
from channels.auth import channel_session_user, channel_session_user_from_http


# Connected to websocket.connect
@channel_session_user_from_http
def ws_add(message, channel):
    message.reply_channel.send({"accept": True})
    Group("chat-%s" % channel).add(message.reply_channel)


# Connected to websocket.receive
@channel_session_user
def ws_message(message, channel):
    Group("chat-%s" % channel).send({
        "text": message['text'] + ":" + message.user.username,
    })


# Connected to websocket.disconnect
@channel_session_user
def ws_disconnect(message, channel):
    Group("chat-%s" % channel).discard(message.reply_channel)
