from sqlmodel import Session
from app.models.category_model import Category
from app.schemas.category.category_schema import CategoryCreate

class CategoryRepository:   
    def __init__(self, session: Session):
        self.session = session

    def create_category(self, category_create: CategoryCreate) -> Category:
        category = Category(**category_create.model_dump())
        self.session.add(category)
        self.session.commit()
        self.session.refresh(category)
        return category

