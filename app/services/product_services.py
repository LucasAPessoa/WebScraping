from uuid import UUID
from fastapi import HTTPException
from sqlmodel import Session
from app.repositories.product_repository import ProductRepository
from app.schemas.product_schema import ProductCreate, ProductUpdate, ProductRead, ProductReadList

class ProductService:
    def __init__(self, session: Session):
        self.repo = ProductRepository(session)

    def create_product(self, data: ProductCreate) -> ProductRead:
        return ProductRead.model_validate(self.repo.create_product(data))

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
