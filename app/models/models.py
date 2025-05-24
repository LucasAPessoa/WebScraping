from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4

class Category(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(index=True, nullable=False)
    
class Promotion(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(index=True, nullable=False)

class Link(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    url: str = Field(index=True, nullable=False)
    
class Establishment(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(index=True, nullable=False)
    url: str = Field(index=True)
    links_id: UUID = Field(foreign_key="link.id")
    
class Photo(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    url: str = Field(index=True, nullable=False)
    product_id: UUID = Field(foreign_key="product_placeholder.id")
    
class Plataform(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(index=True, nullable=False)
    
class ProductPlataform(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    product_placeholder_id: UUID = Field(foreign_key="product_placeholder.id")
    plataform_id: UUID = Field(foreign_key="plataform.id")
    
class Product_Placeholder(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(index=True, nullable=False)
    description: str = Field(index=True, nullable=False)
    category: UUID = Field(foreign_key="category.id")
    metacritic_score: float = Field(index=True, nullable=False)
    plataform: UUID = Field(foreign_key="plataform.id")
    
class Product(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    original_price: float = Field(index=True, nullable=False)
    discounted_price: float = Field(index=True, nullable=False)
    product_placeholder_id: UUID = Field(foreign_key="product_placeholder.id")
    establishment_id: UUID = Field(foreign_key="establishment.id")
    promotion_id: UUID = Field(foreign_key="promotion.id")
    
    @property
    def percentage_discount(self) -> float:
        if self.original_price == 0:
            return 0.0
        return round((1 - self.discounted_price / self.original_price) * 100, 2)