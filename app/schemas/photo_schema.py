from typing import Optional
from uuid import UUID
from pydantic import BaseModel

class PhotoBase(BaseModel):
    url: str
    product_placeholder_id: UUID

class PhotoCreate(PhotoBase):
    pass

class PhotoUpdate(BaseModel):
    url: Optional[str] = None
    product_placeholder_id: Optional[UUID] = None

class PhotoRead(PhotoBase):
    id: UUID

    class Config:
        from_attributes = True

class PhotoReadList(BaseModel):
    photos: list[PhotoRead]
