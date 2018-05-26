from __init__ import redis_conn

def remove_provide(provider_to_remove):
    provider_pool = redis_conn.get('provider_pool').split()
    if provider_to_remove in provider_pool:
        provider_pool.remove(provider_to_remove)
    redis_conn.set('provider_pool', ' '.join(provider_pool))

def add_provide(provider_to_add):
    provider_pool = redis_conn.get('provider_pool').split()
    if provider_to_add not in provider_pool:
        provider_pool.append(provider_to_add)
    redis_conn.set('provider_pool', ' '.join(provider_pool))

