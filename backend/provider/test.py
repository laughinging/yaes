# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import sendgrid
import os
from sendgrid.helpers.mail import *

a = "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"
sg = sendgrid.SendGridAPIClient(apikey=a)
from_email = Email("test@example.com")
to_email = Email("test@example.com")
subject = "Sending with SendGrid is Fun"
content = Content("text/plain", "and easy to do anywhere, even with Python")
mail = Mail(from_email, subject, to_email, content)
response = sg.client.mail.send.post(request_body=mail.get())
print(response.status_code)
print(response.body)
print(response.headers)
