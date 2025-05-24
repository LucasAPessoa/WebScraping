from uuid import UUID, uuid4
from sqlmodel import Session, select

from app.models.models import Category
from app.schemas.category.category_schema import CategoryCreate, CategoryRead, CategoryDelete, CategoryUpdate, CategoryReadList

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
    
    def update_category(self, category_id: UUID, category_update: CategoryUpdate) -> CategoryRead:
        category = self.session.get(Category, category_id)
        
        for key, value in category_update.model_dump().items():
            setattr(category, key, value)
        
        self.session.commit()
        self.session.refresh(category)
        return category

    def delete_category(self, category_delete: CategoryDelete) -> None:
        self.session.delete(category_delete)
        self.session.commit()

    def get_category_by_id(self, category_id: UUID) -> Category | None:
        return self.session.get(Category, category_id)
    
    def get_all_categories(self) -> CategoryReadList:
        return self.session.exec(select(Category)).scalars().all()
    
    def get_category_by_name(self, category_name: str) -> Category | None:
        return self.session.exec(
    select(Category).where(Category.name.ilike(f"%{category_name.lower()}%"))
).first()