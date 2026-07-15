from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.price_history import PriceHistory


async def create(
    db: AsyncSession,
    product_id: int,
    price: Decimal,
) -> PriceHistory:
    """
    Создает запись изменения цены.
    """

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
) -> list[PriceHistory]:
    """
    Возвращает всю историю цен товара.
    """

    result = await db.execute(
        select(PriceHistory)
        .where(
            PriceHistory.product_id == product_id
        )
        .order_by(
            PriceHistory.checked_at.desc()
        )
    )

    return list(
        result.scalars().all()
    )


async def get_latest(
    db: AsyncSession,
    product_id: int,
) -> PriceHistory | None:
    """
    Возвращает последнее изменение цены.
    """

    result = await db.execute(
        select(PriceHistory)
        .where(
            PriceHistory.product_id == product_id
        )
        .order_by(
            PriceHistory.checked_at.desc()
        )
        .limit(1)
    )

    return result.scalar_one_or_none()