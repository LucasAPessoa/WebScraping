from typing import List
from uuid import UUID
from pydantic import BaseModel

class CategoryCreate(BaseModel):
    name: str
    
class CategoryUpdate(BaseModel):
    name: str
        
class CategoryDelete(BaseModel):
    id: str
class CategoryRead(BaseModel):
    id: UUID
    name: str
    
class CategoryReadList(BaseModel):
    categories: List[CategoryRead] 

    class Config:
        from_attributes = True
    