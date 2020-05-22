from django.shortcuts import render

from . import util


def index(request):
    context = {}
    return render(request, 'index.html', context)


def rsvp(request):
    context = {}

    if util.input_submitted(request):
        gc = util.do_rsvp(request)
        print(gc)
        return confirm(request, gc)

    return render(request, 'rsvp.html', context)


def details(request):
    context = {}
    return render(request, 'details.html', context)


def confirm(request, gc):
    context = util.get_rsvp_response(gc)
    return render(request, 'confirm.html', context)
