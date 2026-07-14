from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import price_history_repository


async def get_history(db: AsyncSession, product_id: int):
    return await price_history_repository.get_history(
        db,
        product_id,
    )


async def create_history(
    db: AsyncSession,
    product_id: int,
    price,
):
    return await price_history_repository.create(
        db,
        product_id,
        price,
    )