from urllib.parse import urlparse

from app.schemas.parser import ParsedProduct
from app.services.parsers.base import BaseParser
from app.services.parsers.kaspi import KaspiParser
from app.services.parsers.ozon import OzonParser
from app.services.parsers.wildberries import WildberriesParser


PARSERS: dict[str, BaseParser] = {
    "kaspi.kz": KaspiParser(),
    "www.kaspi.kz": KaspiParser(),

    "ozon.ru": OzonParser(),
    "www.ozon.ru": OzonParser(),

    "wildberries.ru": WildberriesParser(),
    "www.wildberries.ru": WildberriesParser(),
}


async def parse_price(url: str) -> ParsedProduct | None:
    """
    Выбирает парсер и получает данные товара.
    """

    domain = urlparse(url).netloc.lower()

    parser = PARSERS.get(
        domain
    )

    if parser is None:
        return None

    return await parser.parse(
        url
    )