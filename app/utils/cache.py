import redis
import json
from app.core.config import settings

redis_client = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)


def get_cache(key: str):
    data = redis_client.get(key)
    return json.loads(data) if data else None


def set_cache(key: str, value, expire: int = 300):
    redis_client.set(key, json.dumps(value), ex=expire)