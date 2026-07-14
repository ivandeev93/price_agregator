from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import product_repository
from app.schemas.product import ProductCreate, ProductUpdate


async def create_product(
    db: AsyncSession,
    data: ProductCreate,
):
    return await product_repository.create(
        db,
        data,
    )


async def get_product(
    db: AsyncSession,
    product_id: int,
):
    return await product_repository.get_by_id(
        db,
        product_id,
    )


async def get_products(
    db: AsyncSession,
    limit: int = 50,
    offset: int = 0,
):
    return await product_repository.get_all(
        db,
        limit,
        offset,
    )


async def update_product(
    db: AsyncSession,
    product_id: int,
    data: ProductUpdate,
):
    return await product_repository.update_product(
        db,
        product_id,
        data,
    )


async def update_price(
    db: AsyncSession,
    product_id: int,
    price: Decimal,
):
    return await product_repository.update_price(
        db,
        product_id,
        price,
    )


async def delete_product(
    db: AsyncSession,
    product_id: int,
):
    return await product_repository.delete_product(
        db,
        product_id,
    )