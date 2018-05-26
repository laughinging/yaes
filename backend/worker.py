from rq import Worker, Queue, Connection
from __init__ import redis_conn

listen = ['high', 'low']
mail_queue = Queue('default', connection=redis_conn)
provider_updating_queue = Queue('high', connection=redis_conn)

if __name__ == '__main__':
    with Connection():
        w = Worker(map(Queue, listen))
        w.work()

git filter-branch --force --index-filter \
'git rm --cached --ignore-unmatch backend/provider/sendgridservice.py' \
--prune-empty --tag-name-filter cat -- --all
