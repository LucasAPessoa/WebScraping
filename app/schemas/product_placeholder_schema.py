from uuid import UUID
from typing import List
from pydantic import BaseModel

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
    plataform: UUID

    class Config:
        from_attributes = True

class ProductPlaceholderReadList(BaseModel):
    products: List[ProductPlaceholderRead]

    class Config:
        from_attributes = True

class ProductPlaceholderDelete(BaseModel):
    id: UUID

