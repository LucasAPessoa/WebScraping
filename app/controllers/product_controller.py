from sqlmodel import Session
from uuid import UUID
from app.schemas.product_schema import ProductCreate, ProductUpdate, ProductRead, ProductReadList
from app.services.product_services import ProductService

def create_product(product_create: ProductCreate, session: Session) -> ProductRead:
    return ProductService(session).create_product(product_create)

def update_product(product_id: str, product_update: ProductUpdate, session: Session) -> ProductRead:
    return ProductService(session).update_product(product_id, product_update)

def delete_product(product_id: str, session: Session):
    ProductService(session).delete_product(product_id)

def get_product_by_id(product_id: str, session: Session) -> ProductRead:
    return ProductService(session).get_product_by_id(product_id)

def get_all_products(session: Session) -> ProductReadList:
    return ProductService(session).get_all_products()

def filter_products(
    session: Session,
    product_placeholder_id: str = None,
    establishment_id: str = None,
    promotion_id: str = None,
    min_discount: float = None,
    max_discount: float = None
) -> ProductReadList:
    return ProductService(session).filter_product(
        product_placeholder_id,
        establishment_id,
        promotion_id,
        min_discount,
        max_discount
    )
