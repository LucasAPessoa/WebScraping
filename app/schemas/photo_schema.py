from uuid import UUID
from typing import List
from pydantic import BaseModel

class PhotoCreate(BaseModel):
    url: str
    product_placeholder_id: UUID

class PhotoUpdate(BaseModel):
    url: str

class PhotoRead(BaseModel):
    id: UUID
    url: str
    product_placeholder_id: UUID


    class Config:
        from_attributes = True

class PhotoReadList(BaseModel):
    photos: List[PhotoRead]

    class Config:
        from_attributes = True
