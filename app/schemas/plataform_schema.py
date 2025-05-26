from typing import List
from uuid import UUID
from pydantic import BaseModel

class PlataformCreate(BaseModel):
    name: str


class PlataformUpdate(BaseModel):
    name: str


class PlataformDelete(BaseModel):
    id: str


class PlataformRead(BaseModel):
    id: UUID
    name: str

    class Config:
        from_attributes = True


class PlataformReadList(BaseModel):
    plataforms: List[PlataformRead]

    class Config:
        from_attributes = True
