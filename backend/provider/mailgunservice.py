import os
import logging
import requests

from backend.provider.provider_exceptions import *
from set_up import mailgun_api_key 

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class MailgunMail(object):

    MAILGUN_ERROR = {
            400: "BAD REQUEST: Often missing a required parameter", 
            401: "UNAUTHORIZED: No valid API key provided.", 
            402: "Request Failed: Parameters were valid but request failed.",
            404: "NOT FOUND : The requested item doesn't exist.", 
            500: "SERVER Errors: Something is wrong on Mailgun's end.", 
            502: "SERVER Errors: Something is wrong on Mailgun's end.", 
            503: "SERVER Errors: Something is wrong on Mailgun's end.", 
            504: "SERVER Errors: Something is wrong on Mailgun's end.", 
            }

    def __init__(self):
        self.mailgun_api_key = mailgun_api_key

    def send_mail(self, **kwargs):

        from_email = kwargs['sender']
        to_email = kwargs['recipient']
        subject = kwargs['subject']
        text = kwargs['body']

        url = "https://api.mailgun.net/v3/sandboxf15af5beaf6e4a75b7e76a0d11efb08f.mailgun.org/messages"
        logger.info('Attempt to send an email with Mailgun')
        response = requests.post(
                url,
                auth=('api', self.mailgun_api_key),
                data={
                    'from': "mailgun@sandboxf15af5beaf6e4a75b7e76a0d11efb08f.mailgun.org",
                    'to': [to_email],
                    'subject': subject,
                    'text': text
                    }
                )

        status_code = response.status_code
        if status_code in (400, 402, 404):
            message = "Mailgun Client Error {}: {}".format(status_code, 
                    self.MAILGUN_ERROR[status_code])
            logger.exception(message)
            raise ClientError(message)

        elif status_code in (401, 500, 502, 503, 504):
            message = "Mailgun Server Error {}: {}".format(status_code,
                    self.MAILGUN_ERROR[status_code])
            logger.exception(message)
            raise ProviderServerError(message)

if __name__ == "__main__":
    MailgunMail().send_mail(
            sender="test@mailgun.com",
            recipient="qianyunguo@gmail.com", 
            subject="test", 
            body="This is a test email."
            )
