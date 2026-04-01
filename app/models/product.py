from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from app.core.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    url = Column(String, nullable=False)
    target_price = Column(Float, nullable=False)
    current_price = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)