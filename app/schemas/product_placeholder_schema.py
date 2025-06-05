from uuid import UUID
from typing import List, Optional
from pydantic import BaseModel

from app.schemas.photo_schema import PhotoRead
from app.schemas.plataform_schema import PlataformRead

class ProductPlaceholderCreate(BaseModel):
    name: str
    description: str
    category: UUID
    plataform: UUID

class ProductPlaceholderUpdate(BaseModel):
    name: str
    description: str
    category: UUID
    plataform: UUID

class ProductPlaceholderRead(BaseModel):
    id: UUID
    name: str
    description: str
    category: UUID
    metacritic_score: float
    plataforms: Optional[List[PlataformRead]] = [] 
    photos: Optional[List[PhotoRead]] = []

    class Config:
        from_attributes = True

class ProductPlaceholderReadList(BaseModel):
    products: List[ProductPlaceholderRead]

    class Config:
        from_attributes = True

class ProductPlaceholderDelete(BaseModel):
    id: UUID

