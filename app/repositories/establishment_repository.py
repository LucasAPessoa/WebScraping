from sqlalchemy.orm import Session
from app.models.models import Establishment
from app.schemas.establishment_schema import EstablishmentCreate, EstablishmentUpdate, EstablishmentRead
from typing import List, Optional
from uuid import UUID, uuid4

class EstablishmentRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, establishment: EstablishmentCreate) -> Establishment:
        try:
            establishment = Establishment(
                id=str(uuid4()),
                **establishment.model_dump()
            )
            self.db.add(establishment)
            self.db.commit()
            self.db.refresh(establishment)
            return establishment
        except Exception as e:
            self.db.rollback()
            raise e

    def get_by_id(self, establishment_id: UUID) -> Optional[Establishment]:
        return self.db.query(Establishment).filter(Establishment.id == establishment_id).first()

    def get_by_name(self, name: str) -> Optional[Establishment]:
        return self.db.query(Establishment).filter(Establishment.name.ilike(f"%{name}%")).first()

    def get_all(self) -> List[Establishment]:
        return self.db.query(Establishment).all()

    def update(self, establishment_id: UUID, establishment: EstablishmentUpdate) -> Optional[Establishment]:
        db_establishment = self.get_by_id(establishment_id)
        if db_establishment:
            for key, value in establishment.model_dump(exclude_unset=True).items():
                setattr(db_establishment, key, value)
            self.db.commit()
            self.db.refresh(db_establishment)
        return db_establishment

    def delete(self, establishment_id: UUID) -> bool:
        db_establishment = self.get_by_id(establishment_id)
        if db_establishment:
            self.db.delete(db_establishment)
            self.db.commit()
            return True
        return False

    def get_establishment_by_name(self, name: str) -> Optional[Establishment]:
        """Busca um estabelecimento pelo nome"""
        return self.db.query(Establishment).filter(Establishment.name == name).first()

    def get_establishment_by_url(self, url: str) -> Optional[Establishment]:
        """Busca um estabelecimento pela URL"""
        return self.db.query(Establishment).filter(Establishment.website == url).first()
