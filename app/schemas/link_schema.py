from typing import List
from uuid import UUID
from pydantic import BaseModel

class LinkCreate(BaseModel):
    url: str


class LinkUpdate(BaseModel):
    url: str

    
class LinkDelete(BaseModel):
    id: str
    
class LinkRead(BaseModel):
    id: UUID
    url: str


    class Config:
        from_attributes = True
        
class LinkReadList(BaseModel):
    links: List[LinkRead] 

    class Config:
        from_attributes = True