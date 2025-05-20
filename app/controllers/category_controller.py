from fastapi import Depends
from sqlmodel import Session
from app.schemas.category.category_schema import CategoryCreate, CategoryRead
from app.services.category_services import CategoryService
from app.database.session import get_session



def create_category(category_create: CategoryCreate, session: Session):
    service = CategoryService(session)
    return service.create_category(category_create)


def update_category(category_id: str, category_update: CategoryRead, session: Session = Depends(get_session)):
    service = CategoryService(session)
    return service.update_category(category_id, category_update)

def delete_category(category_id: str, session: Session = Depends(get_session)):
    service = CategoryService(session)
    return service.delete_category(category_id)
