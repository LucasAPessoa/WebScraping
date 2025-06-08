from typing import List, Optional
from uuid import UUID, uuid4
from sqlmodel import select
from app.models.models import Product
from app.schemas.product_schema import ProductCreate, ProductUpdate
from sqlalchemy.orm import Session

class ProductRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_product(self, product_create: ProductCreate) -> Product:
        try:
            product = Product(
                id=str(uuid4()),
                **product_create.model_dump()
            )
            self.db.add(product)
            self.db.commit()
            self.db.refresh(product)
            return product
        except Exception as e:
            self.db.rollback()
            raise e

    def get_by_id(self, product_id: str) -> Optional[Product]:
        return self.db.get(Product, product_id)

    def update_product(self, product_id: str, product_update: ProductUpdate) -> Optional[Product]:
        product = self.db.get(Product, product_id)
        if not product:
            return None
        for key, value in product_update.model_dump(exclude_unset=True).items():
            setattr(product, key, value)
        self.db.commit()
        self.db.refresh(product)
        return product

    def delete_product(self, product_id: str) -> None:
        product = self.db.get(Product, product_id)
        if product:
            self.db.delete(product)
            self.db.commit()

    def get_all(self) -> List[Product]:
        return self.db.query(Product).all()

    def filter_products(
        self,
        product_placeholder_id: Optional[str] = None,
        establishment_id: Optional[str] = None,
        promotion_id: Optional[str] = None,
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

        results = self.db.query(Product).filter(statement).all()

        filtered = []
        for product in results:
            discount = product.percentage_discount
            if (min_discount is None or discount >= min_discount) and (max_discount is None or discount <= max_discount):
                filtered.append(product)

        return filtered

    def update_product_promotion(self, product_id: str, promotion_id: Optional[str]) -> None:
        """Atualiza a promoção de um produto"""
        try:
            self.db.query(Product).filter(Product.id == product_id).update(
                {Product.promotion_id: promotion_id}
            )
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e
