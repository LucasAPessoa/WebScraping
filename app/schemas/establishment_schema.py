from typing import List
from uuid import UUID
from pydantic import BaseModel

class EstablishmentCreate(BaseModel):
    name: str
    url: str
    
class EstablishmentUpdate(BaseModel):
    name: str | None = None
    url: str | None = None
    
class EstablishmentDelete(BaseModel):
    id: str
    
class EstablishmentRead(BaseModel):
    id: str
    name: str
    url: str | None = None

    class Config:
        from_attributes = True
        
class EstablishmentReadList(BaseModel):
    establishments: List[EstablishmentRead]

    class Config:
        from_attributes = True