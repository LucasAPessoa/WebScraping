from sqlmodel import Session
from app.models.category_model import Category
from app.schemas.category.category_schema import CategoryCreate
from app.repositories.category_repository import CategoryRepository

class CategoryService:
    def __init__(self, session: Session):
        self.session = session
        self.category_repository = CategoryRepository(session)

    def create_category(self, category_create: CategoryCreate) -> Category:
        
        return self.category_repository.create_category(category_create)