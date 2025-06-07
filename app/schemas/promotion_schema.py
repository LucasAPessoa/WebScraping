from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, Field
from datetime import datetime

from app.schemas.product_schema import ProductRead

class PromotionBase(BaseModel):
    name: str = Field(..., description="Nome da promoção")
    description: Optional[str] = Field(None, description="Descrição da promoção")
    start_date: datetime = Field(..., description="Data de início da promoção")
    end_date: datetime = Field(..., description="Data de término da promoção")
    is_active: bool = Field(True, description="Status da promoção")
    discount_percentage: float = Field(..., description="Percentual de desconto")

class PromotionCreate(PromotionBase):
    pass

class PromotionUpdate(BaseModel):
    name: Optional[str] = Field(None, description="Nome da promoção")
    description: Optional[str] = Field(None, description="Descrição da promoção")
    start_date: Optional[datetime] = Field(None, description="Data de início da promoção")
    end_date: Optional[datetime] = Field(None, description="Data de término da promoção")
    is_active: Optional[bool] = Field(None, description="Status da promoção")
    discount_percentage: Optional[float] = Field(None, description="Percentual de desconto")

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