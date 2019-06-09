from django.shortcuts import render

from . import util


def index(request):
    context = {}
    return render(request, 'index.html', context)


def rsvp(request):
    context = {}

    if util.input_submitted(request):
        errors = util.validate_input(request)
        if not errors:
            return render(request, 'index.html', context)
        else:
            context['errors'] = errors

    context['inputs'] = util.generate_defaults(request)
    return render(request, 'rsvp.html', context)


def details(request):
    context = {}
    return render(request, 'details.html', context)
