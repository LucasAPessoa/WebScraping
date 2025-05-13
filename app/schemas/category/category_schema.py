from typing import NewType
from pydantic import BaseModel, constr, field_validator
from uuid import UUID


CategoryName = NewType("CategoryName", constr(min_length=1, max_length=50))


class CategoryCreate(BaseModel):
    name: CategoryName
    
    @field_validator("name", pre=True)
    def lowercase_name(cls, v):
        if isinstance(v, str):
            return v.lower()
        return v
    
class CategoryRead(BaseModel):
    id: UUID
    name: str

    class Config:
        orm_mode = True
    