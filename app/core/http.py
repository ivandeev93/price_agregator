import asyncio

import httpx


DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/138.0.0.0 Safari/537.36"
    ),
    "Accept": (
        "text/html,application/xhtml+xml,"
        "application/xml;q=0.9,image/webp,*/*;q=0.8"
    ),
    "Accept-Language": "ru-RU,ru;q=0.9,en;q=0.8",
}


limits = httpx.Limits(
    max_connections=20,
    max_keepalive_connections=10,)


client = httpx.AsyncClient(
    timeout=httpx.Timeout(30.0),
    follow_redirects=True,
    headers=DEFAULT_HEADERS,
    http2=True,
    limits=limits,
)


async def get(
    url: str,
    retries: int = 3,
) -> httpx.Response | None:
    """
    GET запрос с повторными попытками.

    Повторяем только временные ошибки:
    - сеть
    - 429
    - 5xx
    """

    for attempt in range(retries):

        try:

            response = await client.get(url)

            if response.status_code == 429:
                await asyncio.sleep(2 ** attempt)
                continue

            if 500 <= response.status_code < 600:
                await asyncio.sleep(2 ** attempt)
                continue

            response.raise_for_status()

            return response

        except httpx.HTTPError:
            if attempt == retries - 1:
                return None

            await asyncio.sleep(2 ** attempt)

    return None


async def close_http():
    """
    Закрытие HTTP клиента.
    """

    await client.aclose()