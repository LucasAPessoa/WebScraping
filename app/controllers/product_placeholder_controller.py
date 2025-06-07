from sqlmodel import Session
from app.services.product_placeholder_services import ProductPlaceholderService
from app.repositories.product_placeholder_repository import ProductPlaceholderRepository
from app.repositories.promotion_repository import PromotionRepository
from app.schemas.product_placeholder_schema import (
    ProductPlaceholderCreate,
    ProductPlaceholderUpdate,
    ProductPlaceholderRead,
    ProductPlaceholderReadList
)
from typing import List
from uuid import UUID

def create_product_placeholder(product_create: ProductPlaceholderCreate, session: Session) -> ProductPlaceholderRead:
    repository = ProductPlaceholderRepository(session)
    promotion_repository = PromotionRepository(session)
    return ProductPlaceholderService(repository, promotion_repository).create_product_placeholder(product_create)

def update_product_placeholder(product_id: UUID, product_update: ProductPlaceholderUpdate, session: Session) -> ProductPlaceholderRead:
    repository = ProductPlaceholderRepository(session)
    promotion_repository = PromotionRepository(session)
    return ProductPlaceholderService(repository, promotion_repository).update_product_placeholder(product_id, product_update)

def delete_product_placeholder(product_id: UUID, session: Session):
    repository = ProductPlaceholderRepository(session)
    promotion_repository = PromotionRepository(session)
    ProductPlaceholderService(repository, promotion_repository).delete_product_placeholder(product_id)

def get_product_placeholder_by_id(product_id: UUID, session: Session) -> ProductPlaceholderRead:
    repository = ProductPlaceholderRepository(session)
    promotion_repository = PromotionRepository(session)
    return ProductPlaceholderService(repository, promotion_repository).get_product_placeholder_by_id(product_id)

def get_all_product_placeholders(session: Session) -> List[ProductPlaceholderReadList]:
    repository = ProductPlaceholderRepository(session)
    promotion_repository = PromotionRepository(session)
    return ProductPlaceholderService(repository, promotion_repository).get_all_product_placeholder()
