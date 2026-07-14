from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.price_history import PriceHistory


async def create(
    db: AsyncSession,
    product_id: int,
    price: Decimal,
):
    history = PriceHistory(
        product_id=product_id,
        price=price,
    )

    db.add(history)

    await db.commit()

    await db.refresh(history)

    return history


async def get_history(
    db: AsyncSession,
    product_id: int,
):
    result = await db.execute(
        select(PriceHistory)
        .where(
            PriceHistory.product_id == product_id
        )
        .order_by(
            PriceHistory.checked_at.desc()
        )
    )

    return list(result.scalars())