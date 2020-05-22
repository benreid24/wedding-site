import re
import logging

from django.core.mail import EmailMessage

from . import models

EMAIL_REGEX = r"[^@]+@([^\.]+\.[^\.]+)+"
logging.basicConfig(filename='errors.log', level=logging.DEBUG)
RSVP_TEMPLATE = """
Name: {name}
Email: {email}
Guest Count: {guests}
Notes: {notes}
"""
RSVP_GOING_TEMPLATE = "Thank you for RSVP'ing! We have you down for {count} guest{pl}. " \
                      "If there are any updates feel free to email us or RSVP again"
RSVP_DENIED_TEMPLATE = 'We are sorry you cannot come. Thank you for letting us know!'
RSVP_ERROR = 'An error has occured. Please try again, or email us with your details'


def _get_guests(data):
    guest_count = int(data['guestCount'])
    guests = []
    for i in range(0, guest_count):
        if f'guest{i}-name' in data.keys():
            guest = {
                'name': data[f'guest{i}-name'],
                'safari': data[f'guest{i}-safari'],
                'meal': data[f'guest{i}-meal']
            }
            guests.append(guest)
    return guests


def input_submitted(request):
    return request.POST


def do_rsvp(request):
    data = request.POST.dict()

    name = data['name']
    email = data['email']
    guests = _get_guests(data)
    notes = data['notes']

    try:
        rsvp = models.Rsvp(family_name=name, email=email, notes=notes)
        rsvp.save()
        print(rsvp.id)
        guest_models = [
            models.Guest(
                rsvp=rsvp,
                name=g['name'],
                meal=g['meal'],
                safari=g['safari']
            ) for g in guests
        ]
        print(guest_models)

        for g in guest_models:
            print(f'saving {g}')
            g.save()

        pdata = {
            'name': name,
            'email': email,
            'guests': len(guests),
            'notes': notes
        }
        #message = EmailMessage(
        #    'Wedding - Guest RSVP',
        #    RSVP_TEMPLATE.format(**pdata),
        #    to=['reidben24@gmail.com', 'anna.kasprzak@daemen.edu'],
        #)
        #message.send(fail_silently=False)
        return len(guests)
    except Exception as exc:
        print(f'{exc}')
        logging.error(f'Error sending rsvp: {str(exc)}\n\nRSVP: {data}')

    return -1


def get_rsvp_response(gc):
    context = {
        'response': RSVP_DENIED_TEMPLATE
    }
    if gc > 0:
        context['response'] = RSVP_GOING_TEMPLATE.format(**{
            'count': gc,
            'pl': 's' if gc > 1 else ''
        })
    elif gc < 0:
        context['response'] = RSVP_ERROR
    return context
