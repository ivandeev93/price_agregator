from pydantic import BaseModel


class ProductCreate(BaseModel):
    name: str
    url: str
    target_price: float


class ProductResponse(ProductCreate):
    id: int
    current_price: float | None

    class Config:
        from_attributes = True