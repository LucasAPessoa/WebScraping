from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.controllers import category_controller
from app.schemas.category_schema import CategoryCreate, CategoryRead, CategoryUpdate, CategoryReadList
from app.database.session import get_session 

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.post("/", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
def create_category(category_create: CategoryCreate, session: Session = Depends(get_session)):
    return category_controller.create_category(category_create, session)

@router.put("/{category_id}", response_model=CategoryRead)
def update_category(category_id: str, category_update: CategoryUpdate, session: Session = Depends(get_session)):
    return category_controller.update_category(category_id, category_update, session)

@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: str, session: Session = Depends(get_session)):
    return category_controller.delete_category(category_id, session)

@router.get("/{category_id}", response_model=CategoryRead)
def get_category_by_id(category_id: str, session: Session = Depends(get_session)):
    return category_controller.get_category_by_id(category_id, session)

@router.get("/", response_model=CategoryReadList)
def get_all_categories(session: Session = Depends(get_session)):
    return category_controller.get_all_categories(session)