from sqlmodel import Session
from app.models.models import Establishment
from app.schemas.establishment_schema import EstablishmentCreate, EstablishmentRead, EstablishmentUpdate, EstablishmentReadList
from app.repositories.establishment_repository import EstablishmentRepository
from fastapi import HTTPException
from uuid import UUID, uuid4
import logging
from typing import List, Optional

logger = logging.getLogger(__name__)

class EstablishmentService:
    def __init__(self, db: Session):
        self.repo = EstablishmentRepository(db)

    def create_establishment(self, establishment: EstablishmentCreate) -> EstablishmentRead:
        """Cria um novo estabelecimento"""
        try:
            # Verifica se já existe um estabelecimento com o mesmo nome
            existing = self.repo.get_by_name(establishment.name)
            if existing:
                raise ValueError(f"Já existe um estabelecimento com o nome '{establishment.name}'")

            # Cria o estabelecimento
            logger.info(f"Criando novo estabelecimento: {establishment.model_dump()}")
            db_establishment = self.repo.create(establishment)
            logger.info(f"Estabelecimento criado com sucesso: {db_establishment.id}")
            return EstablishmentRead.model_validate(db_establishment)
        except Exception as e:
            logger.error(f"Erro ao criar estabelecimento: {str(e)}")
            raise

    def get_establishment(self, establishment_id: UUID) -> Optional[EstablishmentRead]:
        """Busca um estabelecimento pelo ID"""
        db_establishment = self.repo.get_by_id(establishment_id)
        if not db_establishment:
            return None
        return EstablishmentRead.model_validate(db_establishment)

    def get_all_establishments(self) -> EstablishmentReadList:
        """Retorna todos os estabelecimentos"""
        establishments = self.repo.get_all()
        return EstablishmentReadList(
            establishments=[EstablishmentRead.model_validate(est) for est in establishments]
        )

    def update_establishment(self, establishment_id: UUID, establishment: EstablishmentUpdate) -> Optional[EstablishmentRead]:
        """Atualiza um estabelecimento"""
        # Verifica se o estabelecimento existe
        existing = self.repo.get_by_id(establishment_id)
        if not existing:
            return None

        # Se estiver atualizando o nome, verifica se já existe outro com o mesmo nome
        if establishment.name:
            name_exists = self.repo.get_by_name(establishment.name)
            if name_exists and name_exists.id != establishment_id:
                raise ValueError(f"Já existe um estabelecimento com o nome '{establishment.name}'")

        # Atualiza o estabelecimento
        db_establishment = self.repo.update(establishment_id, establishment)
        if not db_establishment:
            return None
        return EstablishmentRead.model_validate(db_establishment)

    def delete_establishment(self, establishment_id: UUID) -> bool:
        """Remove um estabelecimento"""
        return self.repo.delete(establishment_id)

    def get_establishment_by_name(self, name: str) -> Optional[dict]:
        """Busca um estabelecimento pelo nome"""
        try:
            establishment = self.repo.get_by_name(name)
            if not establishment:
                return None
            return EstablishmentRead.from_orm(establishment).dict()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def get_establishment_by_url(self, url: str) -> Optional[dict]:
        """Busca um estabelecimento pela URL"""
        try:
            establishment = self.repo.get_by_url(url)
            if not establishment:
                return None
            return EstablishmentRead.from_orm(establishment).dict()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))