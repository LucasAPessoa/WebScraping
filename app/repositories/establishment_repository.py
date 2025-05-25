from typing import List
from uuid import UUID, uuid4
from sqlmodel import Session, select

from app.models.models import Establishment
from app.schemas.establishment_schema import EstablishmentCreate, EstablishmentRead, EstablishmentUpdate, EstablishmentReadList

class EstablishmentRepository:
    def __init__(self, session: Session):
        self.session = session
        
    def create_establishment(self, establishment_create: EstablishmentCreate) -> EstablishmentRead:
        establishment = Establishment(
            id=uuid4(),
            name=establishment_create.name.strip(),
            url=establishment_create.url.strip() if establishment_create.url else None
        )
        self.session.add(establishment)
        self.session.commit()
        self.session.refresh(establishment)
        return establishment
    
    def get_establishment_by_id(self, establishment_id: UUID) -> Establishment | None:
        return self.session.get(Establishment, establishment_id)
    
    def get_establishment_by_name(self, name: str) -> Establishment | None:
        return self.session.exec(
            select(Establishment).where(Establishment.name.ilike(f"%{name.lower()}%"))
        ).first()
        
    def get_establishment_by_url(self, url: str) -> Establishment | None:
        return self.session.exec(
            select(Establishment).where(Establishment.url.ilike(f"%{url.lower()}%"))
        ).first()
        
    def get_all_establishments(self) -> List[Establishment]:
        result = self.session.exec(select(Establishment))
        return result.all()
    
    def update_establishment(self, establishment_id: UUID, establishment_update: EstablishmentUpdate) -> EstablishmentRead | None:
        establishment = self.session.get(Establishment, establishment_id)
        
        if not establishment:
            return None
        
        for key, value in establishment_update.model_dump(exclude_unset=True).items():
            setattr(establishment, key, value)
        
        self.session.commit()
        self.session.refresh(establishment)
        return establishment
    
    def delete_establishment(self, establishment_id: UUID) -> None:
        establishment = self.session.get(Establishment, establishment_id)
        if establishment:
            self.session.delete(establishment)
            self.session.commit()
