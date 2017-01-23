from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def basic_view(request, buddy):
    return render(request, 'chat/index.html', {
        'buddy': buddy,
    })


def load_conversation(request, buddy):
    pass
