'''

This will assist in creating an email that will contain the details that a
person has been approved by the petitions.

'''


from sendgrid import SendGridClient
from sendgrid import Mail

def sendConfirmation(petitioner, organizer_name, organizer_email):

    #Make a secure connection to SendGrid
    sg = SendGridClient('harmonica1243', '9VwY2sCTuEeYEWpD', secure = True)

    # Make a messsage Object
    message = Mail()

    # Message Subject, perhaps, Petition Passed!
    message.set_subject('Petition Collected Enough Signitures')

    # Replace with the message that we want to send, such as the name of the person and the position
    message.set_html('''<p style="text-align: left;"><font size="4"><b>Dear {!s},</b></font></p>
                     <p style="text-align: left;"><blockquote style="margin: 0 0 0 40px; border: none; padding: 0px;"><p style="text-align: left;">The following applicant has received 25 signatures on his/her petition.</p>
                     <p style="text-align: center;"><b><font size="5"><u style="font-style: normal;">{!s}</u></font></b></p></blockquote>
                     <i>-Petition Application</i></p>'''.format(organizer_name, petitioner)
    message.set_from('petition-app@riceapps.org')

    #Add a recipient
    message.add_to('{!s} <{!s}>'.format(organizer_name, organizer_email))

    # use the Web API to send the message
    sg.send(message)
