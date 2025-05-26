from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.schemas.product_placeholder_schema import (
    ProductPlaceholderCreate,
    ProductPlaceholderUpdate,
    ProductPlaceholderRead,
    ProductPlaceholderReadList
)
from app.controllers import product_placeholder_controller as controller
from app.database.session import get_session

product_placeholder_router = APIRouter(prefix="/products_placeholder", tags=["ProductsPlaceholder"])

@product_placeholder_router.post("/", response_model=ProductPlaceholderRead, status_code=status.HTTP_201_CREATED)
def create_product(data: ProductPlaceholderCreate, session: Session = Depends(get_session)):
    return controller.create_product(data, session)

@product_placeholder_router.get("/", response_model=ProductPlaceholderReadList)
def list_products(session: Session = Depends(get_session)):
    return controller.get_all_products(session)

@product_placeholder_router.get("/{product_id}", response_model=ProductPlaceholderRead)
def get_product(product_id: str, session: Session = Depends(get_session)):
    return controller.get_product_by_id(product_id, session)

@product_placeholder_router.put("/{product_id}", response_model=ProductPlaceholderRead)
def update_product(product_id: str, data: ProductPlaceholderUpdate, session: Session = Depends(get_session)):
    return controller.update_product(product_id, data, session)

@product_placeholder_router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: str, session: Session = Depends(get_session)):
    return controller.delete_product(product_id, session)
