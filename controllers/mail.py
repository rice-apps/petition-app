"""
This will assist in creating an email that will contain the details that a
person has been approved by the petitions.
"""


from sendgrid import SendGridClient
from sendgrid import Mail
from netid2name import netid2name
from config import *


def threshold_met(petitioner_id, organization, election, threshold, position, petition_email, admin_emails):
    petitioner = netid2name(petitioner_id)
    
    # Make a secure connection to SendGrid
    sg = SendGridClient('harmonica1243', 'xqBrrnNqbGuvtEUpNRs3RePW', secure=True)

    # Replace with the message that we want to send, such as the name of the person and the position
    html_petition = '<p style="text-align: left;"><b>Dear ' + petitioner + ',</b></p><p style="text-align: center;">' \
        '<p>Your petition has received the required number of signatures</p><ul><li><b>Organization:</b> ' \
         + organization + '</li><li><b>Election:</b> ' + election + '</li><li><b>Position:</b> ' + position + '</li>' \
        '<li><b>Number of Signatures Required:</b> ' + threshold + '</li></ul><p>Please contact the organization ' \
        'directly with any questions about the petition.</p></p><p style="text-align: left;"><b>Rice Apps Petitions' \
        '</b></p>'
    html_admin = '<p style="text-align: left;"><b>Dear Organization Administrator,</b></p><p style="text-align: center;">' \
        '<p>This petition has received the required number of signatures</p><ul><li><b>Petition Creator:</b> ' \
        + petitioner + '</li><li><b>Organization:</b> ' + organization + '</li><li><b>Election:</b> ' + election + \
        '</li><li><b>Position:</b> ' + position + '</li><li><b>Number of Signatures Required:</b> ' + threshold + \
        '</li></ul><p>Please contact ' + ADMIN_ID + '@rice.edu with any questions.</p></p><p style="text-align: ' \
        'left;"><b>Rice Apps Petitions</b></p>'

    # Make a message Object
    message = Mail()

    # Message Subject, Body and To
    message.set_subject('Petition Collected Enough Signatures')
    message.set_html(html_petition)
    message.set_from('petition-app@riceapps.org')
    message.add_to('<' + petition_email + '>')
    sg.send(message)

    # Make a message Object
    message = Mail()

    # Message Subject, Body and To
    message.set_subject('Petition Collected Enough Signatures')
    message.set_html(html_admin)
    message.set_from('petition-app@riceapps.org')
    for email in admin_emails:
        message.add_to('<' + email + '>')
    sg.send(message)


def threshold_not_met(petitioner_id, organization, election, threshold, signatures, position, petition_email, admin_emails):
    petitioner = netid2name(petitioner_id)

    # Make a secure connection to SendGrid
    sg = SendGridClient('harmonica1243', 'xqBrrnNqbGuvtEUpNRs3RePW', secure=True)

    # Replace with the message that we want to send, such as the name of the person and the position
    html_petition = '<p style="text-align: left;"><b>Dear ' + petitioner + ',</b></p><p style="text-align: center;">' \
        '<p>Your petition no longer has the required number of signatures</p><ul><li><b>Organization:</b> ' \
         + organization + '</li><li><b>Election:</b> ' + election + '</li><li><b>Position:</b> ' + position + '</li>' \
        '<li><b>Number of Signatures Required:</b> ' + threshold + '</li><li><b>Number of Signatures Obtained:</b> ' \
        + signatures + '</li></ul><p>Please contact the organization directly with any questions about the petition.' \
        '</p></p><p style="text-align: left;"><b>Rice Apps Petitions</b></p>'
    html_admin = '<p style="text-align: left;"><b>Dear Organization Administrator,</b></p><p style="text-align: center;">' \
        '<p>This petition no longer has the required number of signatures</p><ul><li><b>Petition Creator:</b> ' \
        + petitioner + '</li><li><b>Organization:</b> ' + organization + '</li><li><b>Election:</b> ' + election + \
        '</li><li><b>Position:</b> ' + position + '</li><li><b>Number of Signatures Required:</b> ' + threshold + \
        '</li><li><b>Number of Signatures Obtained:</b> ' + signatures + '</li></ul><p>Please contact ' + ADMIN_ID + \
        '@rice.edu with any questions.</p></p><p style="text-align: left;"><b>Rice Apps Petitions</b></p>'

    # Make a message Object
    message = Mail()

    # Message Subject, Body and To
    message.set_subject('Petition No Longer Has Enough Signatures')
    message.set_html(html_petition)
    message.set_from('petition-app@riceapps.org')
    message.add_to('<' + petition_email + '>')
    sg.send(message)

    # Make a message Object
    message = Mail()

    # Message Subject, Body and To
    message.set_subject('Petition No Longer Has Enough Signatures')
    message.set_html(html_admin)
    message.set_from('petition-app@riceapps.org')
    for email in admin_emails:
        message.add_to('<' + email + '>')
    sg.send(message)
