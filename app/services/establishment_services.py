from sqlmodel import Session
from app.schemas.establishment_schema import EstablishmentCreate, EstablishmentRead, EstablishmentUpdate, EstablishmentReadList
from app.repositories.establishment_repository import EstablishmentRepository
from fastapi import HTTPException
from uuid import UUID
import re

class EstablishmentService:
    def __init__(self, session: Session):
        self.session = session
        self.establishment_repository = EstablishmentRepository(session)
        
        
    def create_establishment(self, establishment_create: EstablishmentCreate) -> EstablishmentRead:
        name = establishment_create.name.strip()
        if not name:
            raise HTTPException(status_code=400, detail="O nome é obrigatório.")
        
        if len(name) > 100:
            raise HTTPException(status_code=400, detail="O nome deve ter no máximo 100 caracteres.")
        
        url = establishment_create.url.strip() if establishment_create.url else None
        if url and (len(url) > 200 or not re.match(r'^(http|https)://', url)):
            raise HTTPException(status_code=400, detail="O URL deve ter no máximo 200 caracteres e começar com http:// ou https://")
        
        existing_establishment = self.establishment_repository.get_establishment_by_name(name)
        if existing_establishment:
            raise HTTPException(status_code=400, detail="Estabelecimento já existe.")
        
        return self.establishment_repository.create_establishment(establishment_create)
    
    def update_establishment(self, establishment_id: str, establishment_update: EstablishmentUpdate) -> EstablishmentRead:
        try:
            establishment_uuid = UUID(establishment_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="ID de estabelecimento inválido.")
        
        establishment = self.establishment_repository.get_establishment_by_id(establishment_uuid)
        if not establishment:
            raise HTTPException(status_code=404, detail="Estabelecimento não encontrado.")
        
        name = establishment_update.name.strip() if establishment_update.name else None
        if name and (len(name) > 100):
            raise HTTPException(status_code=400, detail="O nome deve ter no máximo 100 caracteres.")
        
        url = establishment_update.url.strip() if establishment_update.url else None
        if url and (len(url) > 200 or not re.match(r'^(http|https)://', url)):
            raise HTTPException(status_code=400, detail="O URL deve ter no máximo 200 caracteres e começar com http:// ou https://")
        
        existing_establishment = self.establishment_repository.get_establishment_by_name(name)
        if existing_establishment and existing_establishment.id != establishment_uuid:
            raise HTTPException(status_code=400, detail="Estabelecimento já existe.")
        
        return self.establishment_repository.update_establishment(establishment_uuid, establishment_update)
    
    def delete_establishment(self, establishment_id: str) -> None:
        try:
            establishment_uuid = UUID(establishment_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="ID de estabelecimento inválido.")
        
        establishment = self.establishment_repository.get_establishment_by_id(establishment_uuid)
        if not establishment:
            raise HTTPException(status_code=404, detail="Estabelecimento não encontrado.")
        
        self.establishment_repository.delete_establishment(establishment_uuid)
        
    def get_establishment_by_id(self, establishment_id: str) -> EstablishmentRead:
        try:
            establishment_uuid = UUID(establishment_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="ID de estabelecimento inválido.")
        
        establishment = self.establishment_repository.get_establishment_by_id(establishment_uuid)
        if not establishment:
            raise HTTPException(status_code=404, detail="Estabelecimento não encontrado.")
        
        return establishment
    
    def get_all_establishments(self) -> EstablishmentReadList:
        establishments = self.establishment_repository.get_all_establishments()
        
        if not establishments:
            raise HTTPException(status_code=404, detail="Nenhum estabelecimento encontrado.")
        
        establishments_read_list = [EstablishmentRead.model_validate(establishment) for establishment in establishments]
        
        return EstablishmentReadList(establishments=establishments_read_list)