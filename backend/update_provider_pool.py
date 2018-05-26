import argparse
from set_up import redis_conn

def remove_provider(provider_to_remove):
    provider_pool = redis_conn.get('provider_pool').split()
    provider_pool = [str(p, 'utf-8') for p in provider_pool]
    if provider_to_remove in provider_pool:
        provider_pool.remove(provider_to_remove)
    redis_conn.set('provider_pool', ' '.join(provider_pool))

def add_provider(provider_to_add):
    provider_pool = redis_conn.get('provider_pool').split()
    provider_pool = [str(p, 'utf-8') for p in provider_pool]
    if provider_to_add not in provider_pool:
        provider_pool.append(provider_to_add)
    redis_conn.set('provider_pool', ' '.join(provider_pool))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            description='Manually update available providers')
    parser.add_argument('-r', nargs='*', help='provider list to remove')
    parser.add_argument('-a', nargs='*', help='provider list to add')
    args = parser.parse_args()

    if args.r is not None:
        map(remove_provider, args.r)
    if args.a is not None:
        map(add_provider, args.a)
    print('current provider: ', redis_conn.get('provider_pool'))
