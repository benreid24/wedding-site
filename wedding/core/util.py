import re
import smtplib
import logging

from django.core.mail import send_mail

EMAIL_REGEX = r"[^@]+@([^\.]+\.[^\.]+)+"
logging.basicConfig(filename='errors.log', level=logging.ERROR)


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
    data = request.POST

    try:
        send_mail(
            'Wedding - Guest RSVP',
            'Here is the message.',
            'rsvp@benanna.love',
            ['reidben24@gmail.com', 'anna.kasprzak@daemen.edu'],
            fail_silently=False,
        )
    except smtplib.SMTPException as exc:
        logging.error(f'Error sending rsvp: {exc}\n\nRSVP: {data}')


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
