import asyncio

from app.core.database import AsyncSessionLocal
from app.repositories.product_repository import get_by_id
from app.services.parser_service import parse_price
from app.services.product_service import update_price
from app.services.price_history_service import create_history
from app.worker.celery_app import celery


@celery.task(
    name="app.tasks.parse_price",
)
def parse_price_task(
    product_id: int,
):
    """
    Celery задача проверки цены товара.
    """

    asyncio.run(
        _parse_price(product_id)
    )


async def _parse_price(
    product_id: int,
):
    """
    Асинхронная логика парсинга.
    """

    async with AsyncSessionLocal() as db:

        product = await get_by_id(
            db,
            product_id,
        )


        if product is None:
            return


        parsed = await parse_price(
            product.url
        )


        if parsed is None:
            return


        new_price = parsed.price


        # Цена не изменилась
        if product.current_price == new_price:
            return


        old_price = product.current_price


        await update_price(
            db,
            product_id,
            new_price,
        )


        await create_history(
            db,
            product_id,
            new_price,
        )


        print(
            f"Product {product_id}: "
            f"{old_price} -> {new_price}"
        )