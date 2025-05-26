from typing import Optional
from uuid import UUID
from pydantic import BaseModel

class ProductCreate(BaseModel):
    original_price: float
    discounted_price: float
    product_placeholder_id: UUID
    establishment_id: UUID
    promotion_id: UUID

class ProductUpdate(BaseModel):
    original_price: Optional[float] = None
    discounted_price: Optional[float] = None
    product_placeholder_id: Optional[UUID] = None
    establishment_id: Optional[UUID] = None
    promotion_id: Optional[UUID] = None

class ProductRead(BaseModel):
    id: UUID
    original_price: float
    discounted_price: float
    product_placeholder_id: UUID
    establishment_id: UUID
    promotion_id: UUID
    percentage_discount: float

    class Config:
        from_attributes = True

class ProductReadList(BaseModel):
    products: list[ProductRead]