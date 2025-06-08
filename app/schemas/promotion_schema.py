from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, Field, field_validator
from datetime import datetime

from app.schemas.product_schema import ProductRead

class PromotionBase(BaseModel):
    name: str = Field(..., description="Nome da promoção")
    description: Optional[str] = Field(None, description="Descrição da promoção")
    min_discount_percentage: float = Field(0.0, description="Percentual mínimo de desconto")
    max_discount_percentage: float = Field(100.0, description="Percentual máximo de desconto")
    

    @field_validator('max_discount_percentage')
    @classmethod
    def validate_max_discount(cls, v, info):
        if 'min_discount_percentage' in info.data and v < info.data['min_discount_percentage']:
            raise ValueError('max_discount_percentage deve ser maior que min_discount_percentage')
        return v

    @field_validator('min_discount_percentage')
    @classmethod
    def validate_min_discount(cls, v):
        if v < 0:
            raise ValueError('min_discount_percentage não pode ser negativo')
        return v

    @field_validator('max_discount_percentage')
    @classmethod
    def validate_max_discount_range(cls, v):
        if v > 100:
            raise ValueError('max_discount_percentage não pode ser maior que 100')
        return v

class PromotionCreate(PromotionBase):
    pass

class PromotionUpdate(BaseModel):
    name: Optional[str] = Field(None, description="Nome da promoção")
    description: Optional[str] = Field(None, description="Descrição da promoção")
    min_discount_percentage: Optional[float] = Field(None, description="Percentual mínimo de desconto")
    max_discount_percentage: Optional[float] = Field(None, description="Percentual máximo de desconto")
    

class PromotionRead(PromotionBase):
    id: str = Field(..., description="ID da promoção")
    products: List["ProductRead"] = Field([], description="Produtos associados")

    class Config:
        from_attributes = True

class PromotionReadList(PromotionBase): 
    id: str = Field(..., description="ID da promoção")

    class Config:
        from_attributes = True

class PromotionDelete(BaseModel):
    message: str = Field(..., description="Mensagem de confirmação")