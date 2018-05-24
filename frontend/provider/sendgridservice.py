import os
import logging
import sendgrid
from sendgrid.helpers.mail import *
from provider_exceptions import *

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class SendgridMail(object):

    SENDGRID_ERROR = {
            400: "BAD REQUEST", 
            401: "UNAUTHORIZED: You do not have authorization to make the request.", 
            403: "FORBIDDEN", 
            404: "NOT FOUND : The resource you tried to locate could not be found or does not exist.", 
            405: "METHOD NOT ALLOWED", 
            413: "PAYLOAD TOO LARGE: The JSON payload you have included in your request is too large.", 
            415: "UNSUPPORTED MEDIA TYPE", 
            429: "TOO MANY REQUESTS: The number of requests you have made exceeds SendGrid’s rate limitations", 
            500: "SERVER UNAVAILABLE: An error occurred on a SendGrid server.", 
            503: "SERVICE NOT AVAILABLE: The SendGrid v3 Web API is not available."
            }

    def __init__(self):
        try:
            #sendgrid_api_key = os.environ.get('SENDGRID_API_KEY')
            sendgrid_api_key = "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"
            self.client = sendgrid.SendGridAPIClient(apikey=sendgrid_api_key)
        except:
            message = "SENDGRID_API_KEY error"
            logger.error(message)
            raise ProviderUnauthorizedError(message)

    def send_mail(self, **kwargs):
        from_email = Email(kwargs['sender'])
        to_email = Email(kwargs['recipient'])
        subject = kwargs['subject']
        content = Content("text/plain", kwargs['body'])

        mail = Mail(from_email, subject, to_email, content)
        logger.info('Attempt to send an email with sendgrid')

        try:
            response = self.client.client.mail.send.post(request_body=mail.get())
        except Exception as e:
            if e.status_code in (400, 401, 403, 404, 405, 413, 415, 429):
                message = "SendGrid Client Error {}: {}".format(e.status_code,
                            self.SENDGRID_ERROR[e.status_code])
                logger.exception(message)
                raise ClientError(message)

            elif response.status_code in (500, 503):
                message =  "SendGrid Server Error {}: {}".format(response.status_code,
                            self.SENDGRID_ERROR[response.status_code])
                logger.exception(message)
                raise ProviderServerError(message)

if __name__ == "__main__":
    SendgridMail().send_mail(
            sender="test@test.com",
            recipient="test@test.com", 
            subject="test", 
            body="This is a test email."
            )
