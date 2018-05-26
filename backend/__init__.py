from redis import Redis
from rq import Worker, Queue, Connection

redis_conn = Redis()
#provider_pool = ['sendgrid', 'sparkpost']
#redis_conn(set, 'provider_pool', ' '.join(provider_pool))
#
mail_queue = Queue('default', connection=redis_conn)
provider_updating_queue = Queue('high', connection=redis_conn)
