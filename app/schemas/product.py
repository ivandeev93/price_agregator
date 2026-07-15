from pydantic import BaseModel, ConfigDict, HttpUrl
from decimal import Decimal
from datetime import datetime


class ProductCreate(BaseModel):
    """
    Схема создания товара.
    """

    name: str
    url: HttpUrl
    target_price: Decimal


class ProductUpdate(BaseModel):
    """
    Схема обновления товара.
    """

    name: str | None = None
    url: HttpUrl | None = None
    target_price: Decimal | None = None


class ProductResponse(BaseModel):
    """
    Схема ответа API.
    """

    id: int
    name: str
    url: HttpUrl
    target_price: Decimal
    current_price: Decimal | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )


# Пример объекта

#{
#  "id": 1,
#  "name": "RTX 5070",
#  "url": "https://shop.com/item",
#  "target_price": "500.00",
#  "current_price": "650.00"
#}