from fastapi import Depends
from sqlmodel import Session
from app.schemas.establishment_schema import EstablishmentCreate, EstablishmentUpdate
from app.services.establishment_services import EstablishmentService
from app.database.session import get_session

def create_establishment(establishment_create: EstablishmentCreate, session: Session):
    service = EstablishmentService(session)
    return service.create_establishment(establishment_create)

def update_establishment(establishment_id: str, establishment_update: EstablishmentUpdate, session: Session = Depends(get_session)):
    service = EstablishmentService(session)
    return service.update_establishment(establishment_id, establishment_update)

def delete_establishment(establishment_id: str, session: Session = Depends(get_session)):
    service = EstablishmentService(session)
    return service.delete_establishment(establishment_id)

def get_establishment_by_id(establishment_id: str, session: Session = Depends(get_session)):
    service = EstablishmentService(session)
    return service.get_establishment_by_id(establishment_id)

def get_all_establishments(session: Session = Depends(get_session)):
    service = EstablishmentService(session)
    return service.get_all_establishments() 

def get_establishment_by_name(establishment_name: str, session: Session = Depends(get_session)):
    service = EstablishmentService(session)
    return service.get_establishment_by_name(establishment_name)

def get_establishment_by_url(establishment_url: str, session: Session = Depends(get_session)):
    service = EstablishmentService(session)
    return service.get_establishment_by_url(establishment_url)