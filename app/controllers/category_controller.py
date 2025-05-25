from fastapi import Depends
from sqlmodel import Session
from app.schemas.category_schema import CategoryCreate, CategoryUpdate
from app.services.category_services import CategoryService
from app.database.session import get_session



def create_category(category_create: CategoryCreate, session: Session):
    service = CategoryService(session)
    return service.create_category(category_create)


def update_category(category_id: str, category_update: CategoryUpdate, session: Session = Depends(get_session)):
    service = CategoryService(session)
    return service.update_category(category_id, category_update)

def delete_category(category_id: str, session: Session = Depends(get_session)):
    service = CategoryService(session)
    return service.delete_category(category_id)

def get_category_by_id(category_id: str, session: Session = Depends(get_session)):
    service = CategoryService(session)
    return service.get_category_by_id(category_id)

def get_all_categories(session: Session = Depends(get_session)):
    service = CategoryService(session)
    return service.get_all_categories()

def get_category_by_name(category_name: str, session: Session = Depends(get_session)):
    service = CategoryService(session)
    return service.get_category_by_name(category_name)