from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import price_history_repository


async def get_history(
    db: AsyncSession,
    product_id: int,
):
    """
    Получение истории изменения цены.
    """

    return await price_history_repository.get_history(
        db,
        product_id,
    )


async def get_latest(
    db: AsyncSession,
    product_id: int,
):
    """
    Получение последнего изменения цены.
    """

    return await price_history_repository.get_latest(
        db,
        product_id,
    )


async def create_history(
    db: AsyncSession,
    product_id: int,
    price: Decimal,
):
    """
    Создание записи в истории цен.
    """

    return await price_history_repository.create(
        db,
        product_id,
        price,
    )