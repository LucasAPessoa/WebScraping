from sqlmodel import Session, select
from typing import List
from uuid import UUID, uuid4

from app.models.models import Photo, Product_Placeholder
from app.schemas.product_placeholder_schema import ProductPlaceholderCreate, ProductPlaceholderUpdate

class ProductPlaceholderRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_product_placeholder(self, product_data: ProductPlaceholderCreate, **game_info) -> Product_Placeholder:
        product = Product_Placeholder(
            id=uuid4(),
            name=product_data.name.strip(),
            description=product_data.description.strip(),
            category=product_data.category,
            plataform=product_data.plataform,
            **game_info
        )
        self.session.add(product)
        self.session.commit()
        self.session.refresh(product)
        return product

    def get_all_product_placeholer(self) -> List[Product_Placeholder]:
        return self.session.exec(select(Product_Placeholder)).all()

    def get_product_placeholder_by_id(self, id: UUID):
        product = self.session.exec(
            select(Product_Placeholder).where(Product_Placeholder.id == id)
        ).one_or_none()

        if product:
            photos = self.session.exec(
                select(Photo).where(Photo.product_placeholder_id == id)
            ).all()
            product.photos = photos
            
            plataforms = self.session.exec(
                select(Product_Placeholder.plataform).where(Product_Placeholder.id == id)
            ).all()
            product.plataforms = plataforms

        return product

    def update_product_placeholer(self, id: UUID, product_data: ProductPlaceholderUpdate, **game_info) -> Product_Placeholder:
        product = self.session.get(Product_Placeholder, id)
        if not product:
            return None

        update_data = product_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            if value is not None:
                setattr(product, key, value)

        for key, value in game_info.items():
            setattr(product, key, value)

        self.session.add(product)
        self.session.commit()
        self.session.refresh(product)
        return product

    def delete_product_placeholer(self, product_id: UUID):
        product = self.session.get(Product_Placeholder, product_id)
        if product:
            self.session.delete(product)
            self.session.commit()
