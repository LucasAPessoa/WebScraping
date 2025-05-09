from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from app.schemas.category.category_schema import CategoryCreate, CategoryRead
from app.services.category_services import CategoryService
from app.database.session import get_session

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.post("/", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
def create_category(category_create: CategoryCreate, session: Session = Depends(get_session)):
    service = CategoryService(session)
    return service.create_category(category_create)