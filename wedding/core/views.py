from django.shortcuts import render
from django.http import HttpResponse

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


def guests(request):
    data = request.GET.dict()
    print(data)
    if 'pw' in data.keys() and data['pw'] == 'thisisliterallymyfavoritemug':
        xml = util.gen_xml()
        response = HttpResponse(xml, content_type='text/xml')
        response['Content-Length'] = len(xml)
        return response
    return render(request, 'denied.html', {})
