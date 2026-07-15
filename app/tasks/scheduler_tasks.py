import asyncio

from sqlalchemy import select

from app.core.database import AsyncSessionLocal
from app.models.product import Product
from app.tasks.price_tasks import parse_price_task
from app.worker.celery_app import celery


@celery.task(
    name="app.tasks.check_all_prices",
)
def check_all_prices_task():
    """
    Запускает проверку цен всех товаров.
    """

    asyncio.run(
        _check_all_prices()
    )


async def _check_all_prices():
    """
    Получает все товары и отправляет
    задачи на проверку цен.
    """

    async with AsyncSessionLocal() as db:

        result = await db.execute(
            select(Product.id)
        )

        product_ids = result.scalars().all()


    for product_id in product_ids:

        parse_price_task.delay(
            product_id
        )