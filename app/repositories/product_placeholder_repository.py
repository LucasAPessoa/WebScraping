from sqlalchemy.orm import Session
from app.models.models import Product_Placeholder
from app.schemas.product_placeholder_schema import ProductPlaceholderCreate, ProductPlaceholderRead, ProductPlaceholderUpdate, ProductPlaceholderUpdateFields
from typing import List, Optional
from uuid import UUID, uuid4

class ProductPlaceholderRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_product_placeholder(self, product_data: ProductPlaceholderUpdateFields) -> Product_Placeholder:
        """Cria um novo produto placeholder"""
        try:
            data = product_data.model_dump()
            data["id"] = str(uuid4())  # Gera o ID aqui
            product = Product_Placeholder(**data)
            self.db.add(product)
            self.db.commit()
            self.db.refresh(product)
            return product
        except Exception as e:
            self.db.rollback()
            raise e

    def get_all_product_placeholder(self) -> List[Product_Placeholder]:
        """Retorna todos os produtos placeholder"""
        return self.db.query(Product_Placeholder).all()

    def get_product_placeholder_by_id(self, product_id: str) -> Optional[Product_Placeholder]:
        """Busca um produto placeholder pelo ID"""
        return self.db.query(Product_Placeholder).filter(Product_Placeholder.id == product_id).first()

    def update_product_placeholder(self, product_id: str, product_data: ProductPlaceholderUpdate) -> Optional[Product_Placeholder]:
        """Atualiza um produto placeholder"""
        try:
            product = self.get_product_placeholder_by_id(product_id)
            if product:
                for key, value in product_data.model_dump(exclude_unset=True).items():
                    setattr(product, key, value)
                self.db.commit()
                self.db.refresh(product)
            return product
        except Exception as e:
            self.db.rollback()
            raise e

    def delete_product_placeholder(self, product_id: str) -> bool:
        """Remove um produto placeholder"""
        try:
            product = self.get_product_placeholder_by_id(product_id)
            if product:
                self.db.delete(product)
                self.db.commit()
                return True
            return False
        except Exception as e:
            self.db.rollback()
            raise e
