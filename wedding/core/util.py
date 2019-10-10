import re
import logging

from django.core.mail import EmailMessage

EMAIL_REGEX = r"[^@]+@([^\.]+\.[^\.]+)+"
logging.basicConfig(filename='errors.log', level=logging.DEBUG)
RSVP_TEMPLATE = """
Name: {name}
Email: {email}
Guest Count: {guests}
Safari Count: {safari}
Meal Option 1: {meal1}
Meal Option 2: {meal2}
Meal Option 3: {meal3}
Notes: {notes}
"""
RSVP_GOING_TEMPLATE = "Thank you for RSVP'ing! We have you down for {count} guest{pl}. " \
                      "If there are any updates feel free to email us or RSVP again"
RSVP_DENIED_TEMPLATE = 'We are sorry you cannot come. Thank you for letting us know!'


def validate_input(request):
    data = request.POST
    errors = {}

    if not data['name']:
        errors['name'] = 'Please input your name'
    if not re.fullmatch(EMAIL_REGEX, data['email']):
        errors['email'] = 'Invalid email address'

    n = int(data['guests'])
    saf = int(data['safari'])
    m1 = int(data['meal1'])
    m2 = int(data['meal2'])
    m3 = int(data['meal3'])

    if saf > n:
        errors['safari'] = 'Too many guests on safari'
    if (m1 + m2 + m3) != n:
        errors['meals'] = 'Meal total must match guest count'

    return errors


def input_submitted(request):
    return request.POST


def do_rsvp(request):
    data = request.POST.dict()

    try:
        message = EmailMessage(
            'Wedding - Guest RSVP',
            RSVP_TEMPLATE.format(**data),
            to=['reidben24@gmail.com', 'anna.kasprzak@daemen.edu'],
        )
        message.send(fail_silently=False)
    except Exception as exc:
        logging.error(f'Error sending rsvp: {str(exc)}\n\nRSVP: {data}')


def generate_defaults(request):
    data = request.POST

    values = {
        'name': '',
        'email': '',
        'notes': ''
    }
    for i in range(0, 7):
        values['guest' + str(i)] = ''
        values['safari' + str(i)] = ''
        values['meal1' + str(i)] = ''
        values['meal2' + str(i)] = ''
        values['meal3' + str(i)] = ''

    if data:
        values['name'] = data['name']
        values['email'] = data['email']
        values['notes'] = data['notes']

        for i in range(0, 7):
            values['guest' + str(i)] = 'selected' if int(data['guests']) == i else ''
            values['safari' + str(i)] = 'selected' if int(data['safari']) == i else ''
            values['meal1' + str(i)] = 'selected' if int(data['meal1']) == i else ''
            values['meal2' + str(i)] = 'selected' if int(data['meal2']) == i else ''
            values['meal3' + str(i)] = 'selected' if int(data['meal3']) == i else ''

    return values


def get_rsvp_response(request):
    data = request.POST.dict()
    context = {
        'name': data['name'],
        'response': RSVP_DENIED_TEMPLATE
    }
    if int(data['guests']) > 0:
        context['response'] = RSVP_GOING_TEMPLATE.format(**{
            'count': data['guests'],
            'pl': 's' if int(data['guests']) > 1 else ''
        })
    return context
