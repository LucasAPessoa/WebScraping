from typing import List, Optional
from uuid import UUID
from sqlmodel import Session, select
from app.models.models import Product
from app.schemas.product_schema import ProductCreate, ProductUpdate

class ProductRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_product(self, product_create: ProductCreate) -> Product:
        product = Product(**product_create.model_dump())
        self.session.add(product)
        self.session.commit()
        self.session.refresh(product)
        return product

    def get_by_id(self, product_id: UUID) -> Optional[Product]:
        return self.session.get(Product, product_id)

    def update_product(self, product_id: UUID, product_update: ProductUpdate) -> Optional[Product]:
        product = self.session.get(Product, product_id)
        if not product:
            return None
        for key, value in product_update.model_dump(exclude_unset=True).items():
            setattr(product, key, value)
        self.session.commit()
        self.session.refresh(product)
        return product

    def delete_product(self, product_id: UUID) -> None:
        product = self.session.get(Product, product_id)
        if product:
            self.session.delete(product)
            self.session.commit()

    def get_all(self) -> List[Product]:
        return self.session.exec(select(Product)).all()

    def filter_products(
        self,
        product_placeholder_id: Optional[UUID] = None,
        establishment_id: Optional[UUID] = None,
        promotion_id: Optional[UUID] = None,
        min_discount: Optional[float] = None,
        max_discount: Optional[float] = None
    ) -> List[Product]:
        statement = select(Product)

        if product_placeholder_id:
            statement = statement.where(Product.product_placeholder_id == product_placeholder_id)
        if establishment_id:
            statement = statement.where(Product.establishment_id == establishment_id)
        if promotion_id:
            statement = statement.where(Product.promotion_id == promotion_id)

        results = self.session.exec(statement).all()

        filtered = []
        for product in results:
            discount = product.percentage_discount
            if (min_discount is None or discount >= min_discount) and (max_discount is None or discount <= max_discount):
                filtered.append(product)

        return filtered
