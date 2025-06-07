from sqlalchemy.orm import Session
from app.models.models import Establishment
from app.schemas.establishment_schema import EstablishmentCreate, EstablishmentUpdate
from typing import List, Optional
from uuid import UUID

class EstablishmentRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_establishment(self, establishment_data: EstablishmentCreate) -> Establishment:
        """Cria um novo estabelecimento"""
        try:
            establishment = Establishment(
                id=establishment_data.id,
                name=establishment_data.name,
                description=establishment_data.description,
                address=establishment_data.address,
                phone=establishment_data.phone,
                email=establishment_data.email,
                website=establishment_data.website
            )
            self.db.add(establishment)
            self.db.commit()
            self.db.refresh(establishment)
            return establishment
        except Exception as e:
            self.db.rollback()
            raise e

    def get_all_establishments(self) -> List[Establishment]:
        """Retorna todos os estabelecimentos"""
        return self.db.query(Establishment).all()

    def get_establishment_by_id(self, establishment_id: str) -> Optional[Establishment]:
        """Busca um estabelecimento pelo ID"""
        return self.db.query(Establishment).filter(Establishment.id == establishment_id).first()

    def update_establishment(self, establishment_id: str, establishment_data: EstablishmentUpdate) -> Optional[Establishment]:
        """Atualiza um estabelecimento"""
        try:
            establishment = self.get_establishment_by_id(establishment_id)
            if not establishment:
                return None

            update_data = establishment_data.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(establishment, key, value)

            self.db.commit()
            self.db.refresh(establishment)
            return establishment
        except Exception as e:
            self.db.rollback()
            raise e

    def delete_establishment(self, establishment_id: str) -> bool:
        """Remove um estabelecimento"""
        try:
            establishment = self.get_establishment_by_id(establishment_id)
            if not establishment:
                return False

            self.db.delete(establishment)
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            raise e

    def get_establishment_by_name(self, name: str) -> Optional[Establishment]:
        """Busca um estabelecimento pelo nome"""
        return self.db.query(Establishment).filter(Establishment.name == name).first()

    def get_establishment_by_url(self, url: str) -> Optional[Establishment]:
        """Busca um estabelecimento pela URL"""
        return self.db.query(Establishment).filter(Establishment.website == url).first()
