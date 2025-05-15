from uuid import UUID
from pydantic import BaseModel

class CategoryCreate(BaseModel):
    name: str
    
class CategoryUpdate(BaseModel):
    id: str
    name: str
        
class CategoryRead(BaseModel):
    id: UUID
    name: str

    class Config:
        from_attributes = True
    