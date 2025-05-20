from sqlmodel import Session
from app.schemas.category.category_schema import CategoryCreate, CategoryRead
from app.repositories.category_repository import CategoryRepository
from fastapi import HTTPException
from uuid import UUID

class CategoryService:
    def __init__(self, session: Session):
        self.session = session
        self.category_repository = CategoryRepository(session)

    def create_category(self, category_create: CategoryCreate) -> CategoryRead:
        
        name = category_create.name.strip().lower()
        if not name:
            raise HTTPException(status_code=400, detail="O nome da categoria é obrigatório.")
        if len(name) < 3:
            raise HTTPException(status_code=400, detail="O nome da categoria deve ter pelo menos 3 caracteres.")
        if len(name) > 50:
            raise HTTPException(status_code=400, detail="O nome da categoria deve ter no máximo 50 caracteres.")
        if not name.isalnum():
            raise HTTPException(status_code=400, detail="O nome da categoria deve conter apenas letras e números.")
        
        
        
        
        return self.category_repository.create_category(category_create)
    
    def update_category(self, category_id: str, category_update: CategoryCreate) -> CategoryRead:
        
        try:
            category_uuid = UUID(category_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="ID de categoria inválido.")

        
        name = category_update.name.strip().lower()
        if not name:
            raise HTTPException(status_code=400, detail="O nome da categoria é obrigatório.")
        if len(name) < 3:
            raise HTTPException(status_code=400, detail="O nome da categoria deve ter pelo menos 3 caracteres.")
        if len(name) > 50:
            raise HTTPException(status_code=400, detail="O nome da categoria deve ter no máximo 50 caracteres.")
        if not name.isalnum():
            raise HTTPException(status_code=400, detail="O nome da categoria deve conter apenas letras e números.")
        
        return self.category_repository.update_category(category_uuid, category_update)
    
    def delete_category(self, category_id: str) -> None:
        try:
            category_uuid = UUID(category_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="ID de categoria inválido.")

        
        category = self.category_repository.get_category_by_id(category_uuid)
        if not category:
            raise HTTPException(status_code=404, detail="Categoria não encontrada.")
        
        return self.category_repository.delete_category(category)