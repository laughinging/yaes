from rq import Worker, Queue, Connection
from set_up import redis_conn

if __name__ == '__main__':
    listen = ['high', 'default']
    with Connection():
        w = Worker(map(Queue, listen))
        w.work()
