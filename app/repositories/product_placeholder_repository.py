from sqlmodel import Session, select
from typing import List
from uuid import UUID, uuid4

from app.models.models import Product_Placeholder
from app.schemas.product_placeholder_schema import ProductPlaceholderCreate, ProductPlaceholderUpdate

class ProductPlaceholderRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_product_placeholer(self, product_data: ProductPlaceholderCreate, metacritic_score: float) -> Product_Placeholder:
        product = Product_Placeholder(
            id=uuid4(),
            name=product_data.name.strip(),
            description=product_data.description.strip(),
            category=product_data.category,
            plataform=product_data.plataform,
            metacritic_score=metacritic_score
        )
        self.session.add(product)
        self.session.commit()
        self.session.refresh(product)
        return product

    def get_all_product_placeholer(self) -> List[Product_Placeholder]:
        return self.session.exec(select(Product_Placeholder)).all()

    def get__product_placeholer_by_id(self, product_id: UUID) -> Product_Placeholder | None:
        return self.session.get(Product_Placeholder, product_id)

    def update_product_placeholer(self, product_id: UUID, product_data: ProductPlaceholderUpdate, metacritic_score: float) -> Product_Placeholder | None:
        product = self.session.get(Product_Placeholder, product_id)
        if not product:
            return None

        product.name = product_data.name.strip()
        product.description = product_data.description.strip()
        product.category = product_data.category
        product.plataform = product_data.plataform
        product.metacritic_score = metacritic_score

        self.session.commit()
        self.session.refresh(product)
        return product

    def delete_product_placeholer(self, product_id: UUID):
        product = self.session.get(Product_Placeholder, product_id)
        if product:
            self.session.delete(product)
            self.session.commit()
