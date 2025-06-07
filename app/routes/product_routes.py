from fastapi import APIRouter, Depends, Query, status
from uuid import UUID
from sqlalchemy.orm import Session
from app.schemas.product_schema import ProductCreate, ProductUpdate, ProductRead, ProductReadList
from app.controllers import product_controller
from app.database.session import get_db

product_router = APIRouter(prefix="/products", tags=["Products"])

@product_router.get("/filter", response_model=ProductReadList)
def filter_products(
    product_placeholder_id: UUID = Query(None),
    establishment_id: UUID = Query(None),
    promotion_id: UUID = Query(None),
    min_discount: float = Query(None),
    max_discount: float = Query(None),
    session: Session = Depends(get_db)
):
    return product_controller.filter_products(
        session,
        product_placeholder_id,
        establishment_id,
        promotion_id,
        min_discount,
        max_discount
    )

@product_router.post("/", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
def create_product(data: ProductCreate, session: Session = Depends(get_db)):
    return product_controller.create_product(data, session)

@product_router.put("/{product_id}", response_model=ProductRead)
def update_product(product_id: UUID, data: ProductUpdate, session: Session = Depends(get_db)):
    return product_controller.update_product(product_id, data, session)

@product_router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: UUID, session: Session = Depends(get_db)):
    product_controller.delete_product(product_id, session)

@product_router.get("/{product_id}", response_model=ProductRead)
def get_product_by_id(product_id: UUID, session: Session = Depends(get_db)):
    return product_controller.get_product_by_id(product_id, session)

@product_router.get("/", response_model=ProductReadList)
def get_all_products(session: Session = Depends(get_db)):
    return product_controller.get_all_products(session)


