from uuid import UUID
from fastapi import HTTPException
from sqlmodel import Session, select
from app.repositories.product_repository import ProductRepository
from app.schemas.product_schema import ProductCreate, ProductUpdate, ProductRead, ProductReadList
from app.models.models import Product, Promotion
from typing import List, Optional

class ProductService:
    def __init__(self, session: Session):
        self.repo = ProductRepository(session)
        self.session = session

    def _find_matching_promotion(self, percentage_discount: float) -> Optional[Promotion]:
        """Encontra uma promoção que corresponda ao percentual de desconto"""
        statement = select(Promotion).where(
            Promotion.min_discount_percentage <= percentage_discount,
            (Promotion.max_discount_percentage >= percentage_discount) | (Promotion.max_discount_percentage.is_(None))
        )
        return self.session.exec(statement).first()

    def create_product(self, product_data: ProductCreate) -> Product:
        """Cria um novo produto e associa automaticamente a uma promoção se aplicável"""
        # Calcula o percentual de desconto
        percentage_discount = ((product_data.original_price - product_data.discounted_price) / product_data.original_price) * 100

        # Encontra uma promoção que corresponda ao desconto
        promotion = self._find_matching_promotion(percentage_discount)

        # Cria o produto com a promoção encontrada (se houver)
        product = Product(
            **product_data.dict(),
            promotion_id=promotion.id if promotion else None
        )

        self.session.add(product)
        self.session.commit()
        self.session.refresh(product)
        return product

    def update_product(self, product_id: UUID, data: ProductUpdate) -> ProductRead:
        product = self.repo.update_product(product_id, data)
        if not product:
            raise HTTPException(status_code=404, detail="Produto não encontrado")
        return ProductRead.model_validate(product)

    def delete_product(self, product_id: UUID):
        if not self.repo.get_by_id(product_id):
            raise HTTPException(status_code=404, detail="Produto não encontrado")
        self.repo.delete_product(product_id)

    def get_product_by_id(self, product_id: UUID) -> ProductRead:
        product = self.repo.get_by_id(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Produto não encontrado")
        return ProductRead.model_validate(product)

    def get_all_products(self) -> ProductReadList:
        return ProductReadList(products=[ProductRead.model_validate(p) for p in self.repo.get_all()])

    def filter_product(
        self,
        product_placeholder_id: UUID = None,
        establishment_id: UUID = None,
        promotion_id: UUID = None,
        min_discount: float = None,
        max_discount: float = None
    ) -> ProductReadList:
        products = self.repo.filter_products(
            product_placeholder_id,
            establishment_id,
            promotion_id,
            min_discount,
            max_discount
        )
        return ProductReadList(products=[ProductRead.model_validate(p) for p in products])
