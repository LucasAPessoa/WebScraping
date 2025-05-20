from uuid import uuid4
from fastapi import HTTPException
from sqlmodel import Session

from app.models.models import Category
from app.schemas.category.category_schema import CategoryCreate, CategoryRead, CategoryDelete, CategoryUpdate

class CategoryRepository:   
    def __init__(self, session: Session):
        self.session = session

    def create_category(self, category_create: CategoryCreate) -> CategoryRead:
        category = Category(
        id=uuid4(),  
        name=category_create.name
    )
        self.session.add(category)
        self.session.commit()
        self.session.refresh(category)
        return category
    
    def update_category(self, category_id: str, category_update: CategoryUpdate) -> CategoryRead:
        category = self.session.get(CategoryRead, category_id)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        
        for key, value in category_update.model_dump().items():
            setattr(category, key, value)
        
        self.session.commit()
        self.session.refresh(category)
        return category

    def delete_category(self, category_delete: CategoryDelete) -> None:
        category = self.session.get(CategoryRead, category_delete)
        self.session.delete(category)
        self.session.commit()
