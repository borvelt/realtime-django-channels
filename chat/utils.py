from functools import wraps
from django.contrib.auth.models import User
from .exceptions import ClientError
import hashlib


def sha256_of(*args):
    channel_users = [arg.username if isinstance(arg, User) else arg for arg in list(args[0])]
    channel_users.sort()
    channel_users = "".join(channel_users)
    return hashlib.sha256(channel_users.encode('utf-8')).hexdigest()


def catch_client_error(func):

    @wraps(func)
    def inner(message, *args, **kwargs):
        try:
            return func(message, *args, **kwargs)
        except ClientError as e:
            e.send_to(message.reply_channel)

    return inner
