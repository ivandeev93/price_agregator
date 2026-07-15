from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class PriceHistoryResponse(BaseModel):
    """
    Ответ с историей изменения цены.
    """

    id: int
    product_id: int
    price: Decimal
    checked_at: datetime

    model_config = ConfigDict(from_attributes=True)