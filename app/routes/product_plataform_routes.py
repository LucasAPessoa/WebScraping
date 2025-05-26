
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database.session import get_session
from app.schemas.product_plataform_schema import ProductPlataformCreate, ProductPlataformRead
from app.controllers import product_plataform_controller as controller
from uuid import UUID

product_plataform_router = APIRouter(prefix="/product-plataform", tags=["ProductPlataform"])

@product_plataform_router.post("/", response_model=ProductPlataformRead, status_code=status.HTTP_201_CREATED)
def create_product_plataform_route(data: ProductPlataformCreate, session: Session = Depends(get_session)):
    return controller.create_product_plataform_controller(data, session)

@product_plataform_router.get("/", response_model=list[ProductPlataformRead])
def get_all_product_plataforms_route(session: Session = Depends(get_session)):
    return controller.get_all_product_plataforms_controller(session)

@product_plataform_router.get("/{relation_id}", response_model=ProductPlataformRead)
def get_product_plataform_by_id_route(relation_id: UUID, session: Session = Depends(get_session)):
    return controller.get_product_plataform_by_id_controller(relation_id, session)

@product_plataform_router.delete("/{relation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product_plataform_route(relation_id: UUID, session: Session = Depends(get_session)):
    controller.delete_product_plataform_controller(relation_id, session)
