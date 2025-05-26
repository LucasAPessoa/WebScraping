
from app.schemas.product_plataform_schema import ProductPlataformCreate
from app.services.product_plataform_service import ProductPlataformService
from sqlalchemy.orm import Session
from uuid import UUID

def create_product_plataform_controller(data: ProductPlataformCreate, session: Session):
    service = ProductPlataformService(session)
    return service.create_product_plataform(data)

def get_all_product_plataforms_controller(session: Session):
    service = ProductPlataformService(session)
    return service.get_all_product_plataforms()

def get_product_plataform_by_id_controller(relation_id: UUID, session: Session):
    service = ProductPlataformService(session)
    return service.get_product_plataform_by_id(relation_id)

def delete_product_plataform_controller(relation_id: UUID, session: Session):
    service = ProductPlataformService(session)
    service.delete_product_plataform(relation_id)
