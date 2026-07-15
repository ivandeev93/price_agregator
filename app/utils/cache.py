import json
from typing import Any

import redis.asyncio as redis
from redis.exceptions import RedisError

from app.core.config import settings


redis_client = redis.from_url(
    settings.REDIS_URL,
    decode_responses=True,
)


async def get_cache(
    key: str,
) -> Any | None:
    """
    Получение значения из Redis.
    """

    try:
        data = await redis_client.get(
            key
        )

    except RedisError:
        return None


    if data is None:
        return None


    try:
        return json.loads(
            data
        )

    except json.JSONDecodeError:
        return None



async def set_cache(
    key: str,
    value: Any,
    expire: int | None = None,
) -> None:
    """
    Сохранение значения в Redis.
    """

    try:
        await redis_client.set(
            key,
            json.dumps(
                value,
                default=str,
            ),
            ex=(
                expire
                or settings.CACHE_EXPIRE_SECONDS
            ),
        )

    except RedisError:
        pass



async def delete_cache(
    key: str,
) -> None:
    """
    Удаление значения из Redis.
    """

    try:
        await redis_client.delete(
            key
        )

    except RedisError:
        pass



async def close_cache() -> None:
    """
    Закрытие Redis соединения.
    """

    await redis_client.aclose()