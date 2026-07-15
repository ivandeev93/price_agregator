import json
from abc import ABC, abstractmethod
from decimal import Decimal

from bs4 import BeautifulSoup

from app.core.http import get
from app.schemas.parser import ParsedProduct


class BaseParser(ABC):
    """
    Базовый класс для всех парсеров.
    """

    async def fetch(self, url: str) -> BeautifulSoup | None:
        """
        Получение HTML страницы.
        """

        response = await get(url)

        if response is None:
            return None

        return BeautifulSoup(
            response.text,
            "html.parser",
        )


    def parse_json_ld_price(
        self,
        soup: BeautifulSoup,
    ) -> Decimal | None:
        """
        Поиск цены в schema.org JSON-LD.
        """

        scripts = soup.find_all(
            "script",
            type="application/ld+json",
        )

        for script in scripts:

            if not script.string:
                continue

            try:
                data = json.loads(
                    script.string
                )

            except Exception:
                continue


            if isinstance(data, list):

                for item in data:

                    price = self.extract_offer_price(
                        item
                    )

                    if price is not None:
                        return price


            elif isinstance(data, dict):

                price = self.extract_offer_price(
                    data
                )

                if price is not None:
                    return price


        return None


    def extract_offer_price(
        self,
        data: dict,
    ) -> Decimal | None:
        """
        Извлекает цену из объекта schema.org.
        """

        offers = data.get("offers")

        if offers is None:
            return None


        if isinstance(
            offers,
            list,
        ):
            offers = offers[0]


        if not isinstance(
            offers,
            dict,
        ):
            return None


        price = offers.get(
            "price"
        )


        if price is None:
            return None


        try:
            return Decimal(
                str(price)
            )

        except Exception:
            return None


    @abstractmethod
    async def parse(self, url: str) -> ParsedProduct | None:
        """
        Метод парсинга конкретного магазина.
        """

        pass