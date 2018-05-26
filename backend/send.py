from __init__ import redis_conn, mail_queue, provider_updating_queue 
from provider import SendgridMail, SparkPostMail
from rq.decorators import job
from update_provider_pool import remove_provide, add_provider

PROVIDER = {
        'sendgrid': SendgridMail,
        'sparkpost': SparkPost
        }

#@job('default', connection=redis_conn)
def send_mail(*args, **kwargs):
    provider_pool = redis_conn.get('provider_pool').split()
    
    sent = False
    for provider_name in provider_pool:
        try:
            PROVIDER[provider_name]().send_mail(**kwargs)
            sent = True
            break

        except ClientError:
            raise InvalidRequestError 

        except ProviderServerError:
            provider_updating_queue.enqueue(remove_provider, provider_name)

    if not sent:
        raise ServerError


            


            





     

