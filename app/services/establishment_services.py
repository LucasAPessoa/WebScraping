from sqlmodel import Session
from app.schemas.establishment_schema import EstablishmentCreate, EstablishmentRead, EstablishmentUpdate, EstablishmentReadList
from app.repositories.establishment_repository import EstablishmentRepository
from fastapi import HTTPException
from uuid import UUID
import re
from typing import List, Optional
from uuid import uuid4

class EstablishmentService:
    def __init__(self, repository: EstablishmentRepository):
        self.repository = repository

    def create_establishment(self, establishment_data: EstablishmentCreate) -> dict:
        """Cria um novo estabelecimento"""
        try:
            # Gera um ID único para o estabelecimento
            establishment_id = str(uuid4())
            
            # Cria o estabelecimento com o ID gerado
            establishment = self.repository.create_establishment(
                EstablishmentCreate(
                    id=establishment_id,
                    **establishment_data.dict()
                )
            )
            
            return EstablishmentRead.from_orm(establishment).dict()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def get_all_establishments(self) -> List[dict]:
        """Retorna todos os estabelecimentos"""
        try:
            establishments = self.repository.get_all_establishments()
            return [EstablishmentReadList.from_orm(establishment).dict() for establishment in establishments]
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def get_establishment_by_id(self, establishment_id: str) -> Optional[dict]:
        """Busca um estabelecimento pelo ID"""
        try:
            establishment = self.repository.get_establishment_by_id(establishment_id)
            if not establishment:
                return None
            return EstablishmentRead.from_orm(establishment).dict()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def update_establishment(self, establishment_id: str, establishment_data: EstablishmentUpdate) -> Optional[dict]:
        """Atualiza um estabelecimento"""
        try:
            establishment = self.repository.update_establishment(establishment_id, establishment_data)
            if not establishment:
                return None
            return EstablishmentRead.from_orm(establishment).dict()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def delete_establishment(self, establishment_id: str) -> bool:
        """Remove um estabelecimento"""
        try:
            return self.repository.delete_establishment(establishment_id)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def get_establishment_by_name(self, name: str) -> Optional[dict]:
        """Busca um estabelecimento pelo nome"""
        try:
            establishment = self.repository.get_establishment_by_name(name)
            if not establishment:
                return None
            return EstablishmentRead.from_orm(establishment).dict()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def get_establishment_by_url(self, url: str) -> Optional[dict]:
        """Busca um estabelecimento pela URL"""
        try:
            establishment = self.repository.get_establishment_by_url(url)
            if not establishment:
                return None
            return EstablishmentRead.from_orm(establishment).dict()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))