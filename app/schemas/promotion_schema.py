from typing import List
from uuid import UUID
from pydantic import BaseModel

class PromotionCreate(BaseModel):
    name: str

class PromotionUpdate(BaseModel):
    name: str
    
class PromotionDelete(BaseModel):
    id: UUID
    
class PromotionRead(BaseModel):
    id: UUID
    name: str

    class Config:
        from_attributes = True
    
class PromotionReadList(BaseModel):
    promotions: List[PromotionRead]

    class Config:
        from_attributes = True