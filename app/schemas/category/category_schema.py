from uuid import UUID
from pydantic import BaseModel, Field

class CategoryCreate(BaseModel):
    name: str= Field(..., description="Name of the category")
    
    
class CategoryRead(BaseModel):
    id: UUID
    name: str

    class Config:
        from_attributes = True
    