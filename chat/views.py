from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def chat_view(request, buddy):
    return render(request, 'chat_view.html', {
        'buddy': buddy,
    })


def load_conversation(request, buddy):
    pass
