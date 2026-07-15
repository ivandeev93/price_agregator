import re
from decimal import Decimal

from bs4 import BeautifulSoup

from app.schemas.parser import ParsedProduct
from app.services.parsers.base import BaseParser


class OzonParser(BaseParser):
    """
    Парсер товаров Ozon.
    """

    async def parse(
        self,
        url: str,
    ) -> ParsedProduct | None:
        """
        Получает данные товара Ozon.
        """

        soup = await self.fetch(
            url
        )

        if soup is None:
            return None


        price = self.parse_json_ld_price(
            soup
        )

        if price is not None:
            return ParsedProduct(
                price=price,
                currency="RUB",
            )


        price = self.parse_html_price(
            soup
        )

        if price is None:
            return None


        return ParsedProduct(
            price=price,
            currency="RUB",
        )


    def parse_html_price(
        self,
        soup: BeautifulSoup,
    ) -> Decimal | None:
        """
        Поиск цены в HTML Ozon.
        """

        text = soup.get_text(
            " ",
            strip=True,
        )


        match = re.search(
            r"(\d[\d\s]*)\s*₽",
            text,
        )


        if match is None:
            return None


        value = (
            match.group(1)
            .replace(
                " ",
                "",
            )
            .replace(
                "\xa0",
                "",
            )
        )


        try:
            return Decimal(
                value
            )

        except Exception:
            return None