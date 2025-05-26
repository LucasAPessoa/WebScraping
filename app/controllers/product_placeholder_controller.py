from fastapi import Depends
from sqlmodel import Session
from app.database.session import get_session
from app.schemas.product_placeholder_schema import (
    ProductPlaceholderCreate,
    ProductPlaceholderUpdate
)
from app.services.product_placeholder_services import ProductPlaceholderService

def create_product(data: ProductPlaceholderCreate, session: Session = Depends(get_session)):
    return ProductPlaceholderService(session).create(data)

def get_all_products(session: Session = Depends(get_session)):
    return ProductPlaceholderService(session).get_all()

def get_product_by_id(product_id: str, session: Session = Depends(get_session)):
    return ProductPlaceholderService(session).get_by_id(product_id)

def update_product(product_id: str, data: ProductPlaceholderUpdate, session: Session = Depends(get_session)):
    return ProductPlaceholderService(session).update(product_id, data)

def delete_product(product_id: str, session: Session = Depends(get_session)):
    return ProductPlaceholderService(session).delete(product_id)
