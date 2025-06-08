from sqlmodel import Session
from uuid import UUID
from app.schemas.establishment_schema import EstablishmentCreate, EstablishmentUpdate, EstablishmentRead, EstablishmentReadList
from app.services.establishment_services import EstablishmentService

def create_establishment(establishment_create: EstablishmentCreate, session: Session) -> EstablishmentRead:
    return EstablishmentService(session).create_establishment(establishment_create)

def update_establishment(establishment_id: str, establishment_update: EstablishmentUpdate, session: Session) -> EstablishmentRead:
    return EstablishmentService(session).update_establishment(establishment_id, establishment_update)

def delete_establishment(establishment_id: str, session: Session):
    EstablishmentService(session).delete_establishment(establishment_id)

def get_establishment_by_id(establishment_id: str, session: Session) -> EstablishmentRead:
    return EstablishmentService(session).get_establishment_by_id(establishment_id)

def get_all_establishments(session: Session) -> EstablishmentReadList:
    return EstablishmentService(session).get_all_establishments()

def filter_establishments(session: Session) -> EstablishmentReadList:
    return EstablishmentService(session).filter_establishments()
