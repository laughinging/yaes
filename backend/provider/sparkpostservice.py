import os
import logging
from provider_exceptions import *
from set_up import sp_client 

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class SparkPostMail(object):

    SPARKPOST_ERROR = {
            400: "BAD REQUEST", 
            401: "UNAUTHORIZED: You do not have authorization to make the request.", 
            403: "FORBIDDEN", 
            404: "NOT FOUND : The resource you tried to locate could not be found or does not exist.", 
            405: "METHOD NOT ALLOWED", 
            413: "PAYLOAD TOO LARGE: The JSON payload you have included in your request is too large.", 
            415: "UNSUPPORTED MEDIA TYPE", 
            429: "TOO MANY REQUESTS: The number of requests you have made exceeds SendGrid's rate limitations",
            500: "SERVER UNAVAILABLE: An error occurred on a SendGrid server.", 
            503: "SERVICE NOT AVAILABLE: The SendGrid v3 Web API is not available."
            }

    def __init__(self):
        self.client = sp_client

    def send_mail(self, **kwargs):
        #from_email = kwargs['sender']
        from_email = "yaes@sparkpostbox.com",
        to_email = kwargs['recipient']
        subject = kwargs['subject']
        text = kwargs['body']

        logger.info('Attempt to send an email with sparkpost')

        response = self.client.transmissions.send(
                use_sandbox=True,
                recipient=[to_email],
                subject=subject,
                text=text)

        print(response.header)

        status_code = response.status_code
        if status_code in (400, 401, 402, 403, 404):
            message = "Mailgun Client Error {}: {}".format(status_code, 
                    self.MAILGUN_ERROR[status_code])
            logger.exception(message)
            raise ClientError(message)

        elif status_code in (500, 502, 503, 504):
            message = "Mailgun Server Error {}: {}".format(status_code,
                    self.MAILGUN_ERROR[status_code])
            logger.exception(message)
            raise ProviderServerError(message) 

if __name__ == "__main__":
    SparkPostMail().send_mail(
            sender="test@test.com",
            recipient="qianyunguo@gmail.com", 
            subject="test", 
            body="This is a test email."
            )





