from fastapi import Depends
from sqlmodel import Session
from app.database.session import get_session
from app.schemas.product_placeholder_schema import (
    ProductPlaceholderCreate,
    ProductPlaceholderUpdate
)
from app.services.product_placeholder_services import ProductPlaceholderService

def create_product_placeholder(data: ProductPlaceholderCreate, session: Session = Depends(get_session)):
    return ProductPlaceholderService(session).create_product_placeholder(data)

def get_all_product_placeholder(session: Session = Depends(get_session)):
    return ProductPlaceholderService(session).get_all_product_placeholder()

def get_product_placeholder_by_id(product_id: str, session: Session = Depends(get_session)):
    return ProductPlaceholderService(session).get_product_placeholder_by_id(product_id)

def update_product_placeholder(product_id: str, data: ProductPlaceholderUpdate, session: Session = Depends(get_session)):
    return ProductPlaceholderService(session).update_product_placeholder(product_id, data)

def delete_product_placeholder(product_id: str, session: Session = Depends(get_session)):
    return ProductPlaceholderService(session).delete_product_placeholder(product_id)
