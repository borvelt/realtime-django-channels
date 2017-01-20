from django.shortcuts import render


def basic_view(request):
    return render(request, 'chat/index.html', {
        'foo': 'bar',
    })
