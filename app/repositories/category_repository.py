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

