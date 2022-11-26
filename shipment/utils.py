from django.conf import settings
from redis import Redis

redis_instance = Redis(host=settings.REDIS_HOST, port=6379, db=0)

def request_is_limited(courier_key: str) -> bool:
    limit = settings.COURIERS_RATELIMITING[courier_key]['requests_number']
    total_seconds = settings.COURIERS_RATELIMITING[courier_key]['waiting_seconds']

    if redis_instance.setnx(courier_key, limit):
        redis_instance.expire(courier_key, int(total_seconds))

    bucket_val = redis_instance.get(courier_key)

    if bucket_val and int(bucket_val) > 0:
        redis_instance.decrby(courier_key, 1)
        return False

    return True