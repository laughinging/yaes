from set_up import redis_conn, mail_queue, provider_updating_queue
from backend.provider.sendgridservice import SendgridMail 
from backend.provider.mailgunservice import MailgunMail 
from backend.update_provider_pool import remove_provider
from backend.exceptions import InvalidRequestError, ServerError
from backend.provider.provider_exceptions import * 

PROVIDER = {
        "sendgrid": SendgridMail,
        "mailgun": MailgunMail
        }

def send_mail(*args, **kwargs):
    provider_pool = redis_conn.get('provider_pool').split()
    provider_pool = [str(p, 'utf-8') for p in provider_pool]

    sent = False
    for provider_name in provider_pool:
        try:
            PROVIDER[provider_name]().send_mail(**kwargs)
            sent = True
            break

        except ClientError as e:
            raise InvalidRequestError(e.description) 

        except ProviderServerError:
            provider_updating_queue.enqueue(remove_provider, provider_name)

    if not sent:
        raise ServerError

if __name__ == "__main__":
    send_mail(
            sender="test@test.com",
            recipient="qianyunguo@gmail.com", 
            subject="test", 
            body="This is a test email."
            )
