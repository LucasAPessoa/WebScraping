from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.controllers import category_controller
from app.schemas.category.category_schema import CategoryCreate, CategoryRead, CategoryUpdate
from app.database.session import get_session 

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.post("/", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
def create_category(category_create: CategoryCreate, session: Session = Depends(get_session)):
    return category_controller.create_category(category_create, session)

@router.put("/{category_id}", response_model=CategoryRead)
def update_category(category_id: str, category_update: CategoryUpdate, session: Session = Depends(get_session)):
    return category_controller.update_category(category_id, category_update, session)