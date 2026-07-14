import asyncio

from app.core.database import AsyncSessionLocal
from app.repositories.product_repository import (
    get_by_id,
    update_price,
)
from app.services.parser_service import parse_price
from app.services.price_history_service import create_history
from app.worker.celery_app import celery


@celery.task(name="app.tasks.parse_price")
def parse_price_task(product_id: int):

    asyncio.run(_parse_price(product_id))


async def _parse_price(product_id: int):
    async with AsyncSessionLocal() as db:

        product = await get_by_id(
            db,
            product_id,
        )

        if product is None:
            return

        new_price = await parse_price(
            product.url,
        )

        if new_price is None:
            return

        # Цена не изменилась — ничего не делаем
        if product.current_price == new_price:
            return

        # Обновляем текущую цену
        await update_price(
            db,
            product_id,
            new_price,
        )

        # Сохраняем изменение в истории
        await create_history(
            db,
            product_id,
            new_price,
        )

        print(
            f"Product {product_id}: "
            f"{product.current_price} -> {new_price}"
        )