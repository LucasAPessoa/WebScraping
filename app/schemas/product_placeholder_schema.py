from uuid import UUID
from typing import List, Optional
from pydantic import BaseModel, Field, validator
import json

from app.schemas.photo_schema import PhotoRead
from app.schemas.plataform_schema import PlataformRead

class ProductPlaceholderBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1, max_length=1000)
    category: UUID
    plataform: UUID

class ProductPlaceholderCreate(ProductPlaceholderBase):
    pass

class ProductPlaceholderUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, min_length=1, max_length=1000)
    category: Optional[UUID] = None
    plataform: Optional[UUID] = None

class ProductPlaceholderRead(ProductPlaceholderBase):
    id: UUID
    metacritic_score: float
    rating: float
    rating_top: int
    released_date: Optional[str] = None
    website: Optional[str] = None
    background_image: Optional[str] = None
    background_image_additional: Optional[str] = None
    genres: Optional[List[str]] = None
    developers: Optional[List[str]] = None
    publishers: Optional[List[str]] = None
    photos: List["PhotoRead"] = []

    @validator('genres', 'developers', 'publishers', pre=True)
    def parse_json_string(cls, v):
        if isinstance(v, str):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return None
        return v

    class Config:
        from_attributes = True

class ProductPlaceholderReadList(BaseModel):
    products: List[ProductPlaceholderRead]

    class Config:
        from_attributes = True

class ProductPlaceholderDelete(BaseModel):
    id: UUID

