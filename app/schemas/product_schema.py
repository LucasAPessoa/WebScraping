from typing import Optional, List
from pydantic import BaseModel, Field
from uuid import UUID

class ProductBase(BaseModel):
    price: float = Field(..., description="Preço original do produto")
    discount_price: Optional[float] = Field(None, description="Preço com desconto")
    url: str = Field(..., description="URL do produto")
    product_placeholder_id: str = Field(..., description="ID do produto placeholder")
    establishment_id: str = Field(..., description="ID do estabelecimento")
    promotion_id: Optional[str] = Field(None, description="ID da promoção associada")

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    price: Optional[float] = Field(None, description="Preço original do produto")
    discount_price: Optional[float] = Field(None, description="Preço com desconto")
    url: Optional[str] = Field(None, description="URL do produto")
    product_placeholder_id: Optional[str] = Field(None, description="ID do produto placeholder")
    establishment_id: Optional[str] = Field(None, description="ID do estabelecimento")
    promotion_id: Optional[str] = Field(None, description="ID da promoção associada")

class ProductRead(ProductBase):
    id: str = Field(..., description="ID do produto")

    class Config:
        orm_mode = True

class ProductReadList(BaseModel):
    products: List[ProductRead] = Field(..., description="Lista de produtos")
