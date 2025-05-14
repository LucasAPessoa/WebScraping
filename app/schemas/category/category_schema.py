from typing import Annotated
from pydantic import BaseModel, constr, field_validator
from uuid import UUID


NameType = Annotated[str, constr(min_length=1, max_length=50)]

class CategoryCreate(BaseModel):
    name: NameType
    
    @field_validator("name", mode="before")
    def lowercase_name(cls, v):
        if isinstance(v, str):
            return v.lower()
        return v
    
class CategoryRead(BaseModel):
    id: UUID
    name: str

    class Config:
        from_attributes = True
    