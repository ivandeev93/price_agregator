from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate

from app.schemas.price_history import PriceHistoryResponse

from app.services import product_service, price_history_service

from app.tasks.price_tasks import parse_price_task

from app.utils.cache import get_cache, set_cache, delete_cache


router = APIRouter()


@router.post(
    "/",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_product(
    data: ProductCreate,
    db: AsyncSession = Depends(get_db),
):
    """
    Создание товара.
    """

    product = await product_service.create_product(
        db,
        data,
    )

    parse_price_task.delay(
        product.id
    )

    return product



@router.get(
    "/",
    response_model=list[ProductResponse],
)
async def get_products(
    limit: int = 50,
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
):
    """
    Получение списка товаров.
    """

    return await product_service.get_products(
        db,
        limit,
        offset,
    )



@router.get(
    "/{product_id}",
    response_model=ProductResponse,
)
async def get_product(
    product_id: int,
    db: AsyncSession = Depends(get_db),
):
    """
    Получение товара по ID.
    """

    cache_key = f"product:{product_id}"


    cached = await get_cache(
        cache_key
    )

    if cached:
        return cached


    product = await product_service.get_product(
        db,
        product_id,
    )


    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )


    response = ProductResponse.model_validate(
        product
    )


    await set_cache(
        cache_key,
        response.model_dump(
            mode="json"
        ),
    )


    return response



@router.get(
    "/{product_id}/history",
    response_model=list[PriceHistoryResponse],
)
async def get_price_history(
    product_id: int,
    db: AsyncSession = Depends(get_db),
):
    """
    Получение истории изменения цены.
    """

    product = await product_service.get_product(
        db,
        product_id,
    )


    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )


    return await price_history_service.get_history(
        db,
        product_id,
    )



@router.patch(
    "/{product_id}",
    response_model=ProductResponse,
)
async def update_product(
    product_id: int,
    data: ProductUpdate,
    db: AsyncSession = Depends(get_db),
):
    """
    Обновление товара.
    """

    product = await product_service.update_product(
        db,
        product_id,
        data,
    )


    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )


    await delete_cache(
        f"product:{product_id}"
    )


    return product



@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_product(
    product_id: int,
    db: AsyncSession = Depends(get_db),
):
    """
    Удаление товара.
    """

    deleted = await product_service.delete_product(
        db,
        product_id,
    )


    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )


    await delete_cache(
        f"product:{product_id}"
    )


    return None