from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.product import ProductCreate, ProductResponse
from app.services.product_service import create_product, get_product
from app.utils.cache import get_cache, set_cache

router = APIRouter()


@router.post("/", response_model=ProductResponse)
def create(data: ProductCreate, db: Session = Depends(get_db)):
    return create_product(db, data)


@router.get("/{product_id}", response_model=ProductResponse)
def read(product_id: int, db: Session = Depends(get_db)):
    cache_key = f"product:{product_id}"

    cached = get_cache(cache_key)
    if cached:
        return cached

    product = get_product(db, product_id)

    if product:
        set_cache(cache_key, ProductResponse.model_validate(product).dict())

    return product