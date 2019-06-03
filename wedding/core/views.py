from django.shortcuts import render


def index(request):
    context = {}
    return render(request, 'index.html', context)


def rsvp(request):
    context = {}
    return render(request, 'rsvp.html', context)
