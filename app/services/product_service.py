from sqlalchemy.orm import Session
from app.models.product import Product


def create_product(db: Session, data):
    product = Product(**data.dict())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def get_product(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()