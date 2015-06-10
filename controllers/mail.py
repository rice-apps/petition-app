"""
This will assist in creating an email that will contain the details that a
person has been approved by the petitions.
"""


from sendgrid import SendGridClient
from sendgrid import Mail
from netid2name import netid2name


def sendConfirmation(petitioner_id, organizer_name, organizer_email):
    petitioner = netid2name(petitioner_id)
    
    # Make a secure connection to SendGrid
    sg = SendGridClient('harmonica1243', 'xqBrrnNqbGuvtEUpNRs3RePW', secure=True)

    # Make a messsage Object
    message = Mail()

    # Message Subject, perhaps, Petition Passed!
    message.set_subject('Petition Collected Enough Signitures')

    # Replace with the message that we want to send, such as the name of the person and the position
    message.set_html('''<p style="text-align: left;"><font size="4"><b>Dear {!s},</b></font></p>
                     <p style="text-align: left;"><blockquote style="margin: 0 0 0 40px; border: none; padding: 0px;">
                     <p style="text-align: left;">The following applicant has received 25 signatures on his/her
                     petition.</p><p style="text-align: center;"><b><font size="5"><u style="font-style: normal;">
                     {!s}</u></font></b></p></blockquote>
                     <i>-Petition Application</i></p>'''.format(organizer_name, petitioner))
    message.set_from('petition-app@riceapps.org')

    # Send message to Organizer
    message.add_to('{!s} <{!s}>'.format(organizer_name, organizer_email))
    # Send message to petitioner
    message.add_to('{!s} <{!s}>'.format(petitioner, petitioner_id + '@rice.edu'))

    # use the Web API to send the message
    sg.send(message)
