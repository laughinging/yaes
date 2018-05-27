import os
import logging
import redis
import requests

from sendgrid import SendGridAPIClient
from sparkpost import SparkPost

from rq import Queue, Connection

# logging setting
logfile = logging.FileHandler('set_up.log')
logging_format = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(filename)s'
        '- %(funcName)s - %(lineno)s - %(message)s')

logfile.setFormatter(logging_format) 
logfile.setLevel(logging.DEBUG)

logger = logging.getLogger(__name__)
logger.addHandler(logfile)

# set up redis server
redis_conn = redis.StrictRedis(host='localhost', port=6379) 
try:
    redis_conn.ping()
except redis.exceptions.ConnectionError:
    message = "Redis server isn't running."
    logger.error("Redis server isn't running")
    raise RuntimeError(message)

# set up mail service provider - SendGrid
sendgrid_api_key = os.environ.get('SENDGRID_API_KEY')

if sendgrid_api_key is None:
    message = ("Failed to set up SendGrid service."
            "Check environment variable SENDGRID_API_KEY")
    logger.error(message)
    raise RuntimeError(message)

sg_client = SendGridAPIClient(apikey=sendgrid_api_key)

# set up mail service provide - Mailgun
mailgun_api_key = os.environ.get('MAILGUN_API_KEY')

if mailgun_api_key is None:
    message = ("Failed to set up Mailgun service."
            "Check environment variable MAILGUN_API_KEY")
    logger.error(message)
    raise RuntimeError(message)

# set up mail queue and updating queue
mail_queue = Queue('default', connection=redis_conn)
provider_updating_queue = Queue('high', connection=redis_conn)

if __name__ == "__main__":
    # set up default mail service provider in redis
    provider_pool = ['sendgrid', 'mailgun']
    redis_conn.set('provider_pool', ' '.join(provider_pool))


