from decimal import Decimal

from pydantic import BaseModel


class ParsedProduct(BaseModel):
    """
    Результат работы любого парсера.
    * Есть возможность расширить данные.
    """

    price: Decimal
    currency: str = "KZT"
    title: str | None = None
    in_stock: bool = True
    image_url: str | None = None