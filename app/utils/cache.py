import redis.asyncio as redis
import json
from app.core.config import settings
from typing import Any


redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)


async def get_cache(key: str) -> Any | None:

    data = await redis_client.get(key)

    if not data:
        return None

    return json.loads(data)


async def set_cache(
    key: str,
    value: Any,
    expire: int | None = None,
):
    await redis_client.set(
        key,
        json.dumps(value),
        ex=expire or settings.CACHE_EXPIRE_SECONDS,
    )


async def delete_cache(key: str):
    await redis_client.delete(key)


async def close_cache():
    await redis_client.close()