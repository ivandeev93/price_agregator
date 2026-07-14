from decimal import Decimal

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate


async def create(
    db: AsyncSession,
    data: ProductCreate,
) -> Product:
    product = Product(
        name=data.name,
        url=str(data.url),
        target_price=data.target_price,
    )

    db.add(product)

    await db.commit()
    await db.refresh(product)

    return product


async def get_by_id(
    db: AsyncSession,
    product_id: int,
) -> Product | None:
    result = await db.execute(
        select(Product)
        .where(Product.id == product_id)
    )

    return result.scalar_one_or_none()


async def get_all(
    db: AsyncSession,
    limit: int = 50,
    offset: int = 0,
) -> list[Product]:
    result = await db.execute(
        select(Product)
        .offset(offset)
        .limit(limit)
        .order_by(Product.created_at.desc())
    )

    return list(result.scalars().all())


async def update_product(
    db: AsyncSession,
    product_id: int,
    data: ProductUpdate,
) -> Product | None:

    values = data.model_dump(
        exclude_unset=True
    )

    if "url" in values:
        values["url"] = str(values["url"])

    if not values:
        return await get_by_id(db, product_id)

    await db.execute(
        update(Product)
        .where(Product.id == product_id)
        .values(**values)
    )

    await db.commit()

    return await get_by_id(db, product_id)


async def update_price(db: AsyncSession, product_id: int,
                       price: Decimal) -> None:

    await db.execute(
        update(Product)
        .where(Product.id == product_id)
        .values(
            current_price=price
        )
    )

    await db.commit()



async def delete_product(
    db: AsyncSession,
    product_id: int,
) -> bool:

    result = await db.execute(
        delete(Product)
        .where(Product.id == product_id)
    )

    await db.commit()

    return result.rowcount > 0