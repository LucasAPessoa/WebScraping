from fastapi import HTTPException
from sqlmodel import Session

from app.schemas.category.category_schema import CategoryCreate, CategoryRead

class CategoryRepository:   
    def __init__(self, session: Session):
        self.session = session

    def create_category(self, category_create: CategoryCreate) -> CategoryRead:
        category = CategoryRead(**category_create.model_dump())
        self.session.add(category)
        self.session.commit()
        self.session.refresh(category)
        return category
    
    def update_category(self, category_id: str, category_update: CategoryCreate) -> CategoryRead:
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
