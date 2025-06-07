from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field
from datetime import datetime

class ProductBase(BaseModel):
    name: str = Field(..., description="Nome do produto")
    description: Optional[str] = Field(None, description="Descrição do produto")
    price: float = Field(..., description="Preço original do produto")
    discount_price: Optional[float] = Field(None, description="Preço com desconto")
    url: Optional[str] = Field(None, description="URL do produto")
    image_url: Optional[str] = Field(None, description="URL da imagem do produto")
    product_placeholder_id: str = Field(..., description="ID do produto placeholder")
    establishment_id: str = Field(..., description="ID do estabelecimento")
    promotion_id: Optional[str] = Field(None, description="ID da promoção")

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, description="Nome do produto")
    description: Optional[str] = Field(None, description="Descrição do produto")
    price: Optional[float] = Field(None, description="Preço original do produto")
    discount_price: Optional[float] = Field(None, description="Preço com desconto")
    url: Optional[str] = Field(None, description="URL do produto")
    image_url: Optional[str] = Field(None, description="URL da imagem do produto")
    product_placeholder_id: Optional[str] = Field(None, description="ID do produto placeholder")
    establishment_id: Optional[str] = Field(None, description="ID do estabelecimento")
    promotion_id: Optional[str] = Field(None, description="ID da promoção")

class ProductRead(ProductBase):
    id: str = Field(..., description="ID do produto")
    percentage_discount: float = Field(..., description="Percentual de desconto")

    class Config:
        from_attributes = True

class ProductReadList(ProductBase):
    id: str = Field(..., description="ID do produto")
    percentage_discount: float = Field(..., description="Percentual de desconto")

    class Config:
        from_attributes = True

class ProductDelete(BaseModel):
    message: str = Field(..., description="Mensagem de confirmação")