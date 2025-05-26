
from app.repositories.product_plataform_repository import ProductPlataformRepository
from app.schemas.product_plataform_schema import ProductPlataformCreate, ProductPlataformRead
from fastapi import HTTPException
from uuid import UUID

class ProductPlataformService:
    def __init__(self, session):
        self.repository = ProductPlataformRepository(session)

    def create_product_plataform(self, data: ProductPlataformCreate) -> ProductPlataformRead:
        created = self.repository.create_product_plataform(data)
        return ProductPlataformRead.model_validate(created)

    def get_all_product_plataforms(self) -> list[ProductPlataformRead]:
        all_relations = self.repository.get_all_product_plataforms()
        return [ProductPlataformRead.model_validate(r) for r in all_relations]

    def get_product_plataform_by_id(self, relation_id: UUID) -> ProductPlataformRead:
        relation = self.repository.get_product_plataform_by_id(relation_id)
        if not relation:
            raise HTTPException(status_code=404, detail="Relação não encontrada.")
        return ProductPlataformRead.model_validate(relation)

    def delete_product_plataform(self, relation_id: UUID):
        relation = self.repository.get_product_plataform_by_id(relation_id)
        if not relation:
            raise HTTPException(status_code=404, detail="Relação não encontrada.")
        self.repository.delete_product_plataform(relation_id)
