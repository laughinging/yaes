import os
import logging
import redis

from sendgrid import SendGridAPIClient
from rq import Worker, Queue, Connection



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
except ConnectionError:
    message = "Redis server isn't running."
    logger.error("Redis server isn't running")
    raise RuntimeError(message)


# set up default mail service provider in redis
provider_pool = ['sendgrid', 'sparkpost']
redis_conn.set('provider_pool', ' '.join(provider_pool))

# set up mail service provider - SendGrid
sendgrid_api_key = os.environ.get('SENDGRID_API_KEY')

if sendgrid_api_key is None:
    message = ("Failed to set up SendGrid service."
            "Check environment variable SENDGRID_API_KEY")
    logger.error(message)
    raise RuntimeError(message)

sg_client = SendGridAPIClient(apikey=sendgrid_api_key)

# set up mail service provide - SparkPost
sparkpost_api_key = os.environ.get('SPARKPOST_API_KEY')

if sparkpost_api_key is None:
    message = ("Failed to set up SparkPost service."
            "Check environment variable SPARKPOST_API_KEY")
    logger.error(message)
    raise RuntimeError(message)

sp_client = SparkPost(sparkpost_api_key)






