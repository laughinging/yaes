from rq import Worker, Queue, Connection
from __init__ import redis_conn

listen = ['high', 'low']
if __name__ == '__main__':
    with Connection():
        w = Worker(map(Queue, listen))
        w.work()


