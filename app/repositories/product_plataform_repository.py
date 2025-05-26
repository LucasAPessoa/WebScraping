
from sqlmodel import Session, select
from app.models.models import ProductPlataform
from app.schemas.product_plataform_schema import ProductPlataformCreate
from uuid import UUID

class ProductPlataformRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_product_plataform(self, data: ProductPlataformCreate) -> ProductPlataform:
        new_relation = ProductPlataform(**data.model_dump())
        self.session.add(new_relation)
        self.session.commit()
        self.session.refresh(new_relation)
        return new_relation

    def get_all_product_plataforms(self) -> list[ProductPlataform]:
        return self.session.exec(select(ProductPlataform)).all()

    def get_product_plataform_by_id(self, relation_id: UUID) -> ProductPlataform | None:
        return self.session.get(ProductPlataform, relation_id)

    def delete_product_plataform(self, relation_id: UUID) -> None:
        relation = self.get_product_plataform_by_id(relation_id)
        if relation:
            self.session.delete(relation)
            self.session.commit()
