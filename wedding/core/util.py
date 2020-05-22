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

XML_TEMPLATE = """<?xml version="1.0" encoding="UTF-8"?>
<?mso-application progid="Excel.Sheet"?>
<Workbook xmlns="urn:schemas-microsoft-com:office:spreadsheet" xmlns:x="urn:schemas-microsoft-com:office:excel" xmlns:ss="urn:schemas-microsoft-com:office:spreadsheet" xmlns:html="https://www.w3.org/TR/html401/">
<Worksheet ss:Name="RSVP's">
<Table>
<Column ss:AutoFitWidth="1"/>
<Row>
<Cell><Data ss:Type="String">Name</Data></Cell>
<Cell><Data ss:Type="String">Email</Data></Cell>
<Cell><Data ss:Type="String">Notes</Data></Cell>
<Cell><Data ss:Type="String">Guest Count</Data></Cell>
</Row>
{rsvp_rows}
</Table>
</Worksheet>
<Worksheet ss:Name="Guests">
<Table>
<Column ss:AutoFitWidth="1"/>
<Row>
<Cell><Data ss:Type="String">Name</Data></Cell>
<Cell><Data ss:Type="String">Family Name</Data></Cell>
<Cell><Data ss:Type="String">Meal</Data></Cell>
<Cell><Data ss:Type="String">Riding Safari</Data></Cell>
<Cell><Data ss:Type="String">SafBool</Data></Cell>
</Row>
{guest_rows}
</Table>
</Worksheet>
</Workbook>
"""
RSVP_XML = """
<Row>
<Cell><Data ss:Type="String">{name}</Data></Cell>
<Cell><Data ss:Type="String">{email}</Data></Cell>
<Cell><Data ss:Type="String">{notes}</Data></Cell>
<Cell><Data ss:Type="String">{guests}</Data></Cell>
</Row>
"""
GUEST_XML = """
<Row>
<Cell><Data ss:Type="String">{name}</Data></Cell>
<Cell><Data ss:Type="String">{fname}</Data></Cell>
<Cell><Data ss:Type="String">{meal}</Data></Cell>
<Cell><Data ss:Type="String">{safari}</Data></Cell>
<Cell><Data ss:Type="String">{safbool}</Data></Cell>
</Row>
"""

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


def _prep_string(string):
    string = string.replace('&', '&amp;')
    return string


def input_submitted(request):
    return request.POST


def do_rsvp(request):
    data = request.POST.dict()

    name = data['name']
    email = data['email']
    guests = _get_guests(data)
    notes = data['notes']

    pdata = {}
    gc = -1

    try:
        rsvp = models.Rsvp(family_name=name, email=email, notes=notes)
        rsvp.save()
        guest_models = [
            models.Guest(
                rsvp=rsvp,
                name=g['name'],
                meal=g['meal'],
                safari=g['safari']
            ) for g in guests
        ]
        for g in guest_models:
            g.save()

        pdata = {
            'name': name,
            'email': email,
            'guests': len(guests),
            'notes': notes
        }
        gc = len(guests)
    except Exception as exc:
        logging.error(f'Error sending rsvp: {str(exc)}\n\nRSVP: {data}')
        return -1

    try:
        message = EmailMessage(
            'Wedding - Guest RSVP',
            RSVP_TEMPLATE.format(**pdata),
            to=['reidben24@gmail.com', 'anna.kasprzak@daemen.edu'],
        )
        message.send(fail_silently=False)
        return gc
    except Exception as exc:
        logging.error(f'Error sending rsvp: {str(exc)}\n\nRSVP: {data}')
        return

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


def gen_xml():
    try:
        rsvps = models.Rsvp.objects.all()
        guest_sets = [
            rsvp.guest_set.all() for rsvp in rsvps
        ]
        guests = []
        for rset in guest_sets:
            guests.extend(rset)

        rsvp_dicts = [
            {
                'name': _prep_string(rsvp.family_name),
                'email': _prep_string(rsvp.email),
                'notes': _prep_string(rsvp.notes),
                'guests': len(rsvp.guest_set.all())
            } for rsvp in rsvps
        ]
        rsvp_rows = '\n'.join([
            RSVP_XML.format(**rsvp) for rsvp in rsvp_dicts
        ])

        guest_dicts = [
            {
                'name': _prep_string(g.name),
                'fname': _prep_string(g.rsvp.family_name),
                'meal': _prep_string(g.meal),
                'safari': _prep_string(g.safari),
                'safbool': '1' if g.safari == 'Yes: Riding' else '0'
            } for g in guests
        ]
        guest_rows = '\n'.join([
            GUEST_XML.format(**g) for g in guest_dicts
        ])

        xml = XML_TEMPLATE.format(rsvp_rows=rsvp_rows, guest_rows=guest_rows)
        return xml
    except Exception as exc:
        logging.error(f'{exc}')

    return ''