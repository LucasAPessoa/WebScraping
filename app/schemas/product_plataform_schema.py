
from pydantic import BaseModel
from uuid import UUID

class ProductPlataformCreate(BaseModel):
    product_placeholder_id: UUID
    plataform_id: UUID

class ProductPlataformRead(ProductPlataformCreate):
    id: UUID
