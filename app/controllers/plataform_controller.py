from fastapi import Depends
from sqlmodel import Session
from app.schemas.plataform_schema import PlataformCreate, PlataformUpdate
from app.services.plataform_services import PlataformService
from app.database.session import get_session

def create_plataform(plataform_create: PlataformCreate, session: Session = Depends(get_session)):
    service = PlataformService(session)
    return service.create_plataform(plataform_create)

def get_plataform_by_id(plataform_id: str, session: Session = Depends(get_session)):
    service = PlataformService(session)
    return service.get_plataform_by_id(plataform_id)

def get_all_plataforms(session: Session = Depends(get_session)):
    service = PlataformService(session)
    return service.get_all_plataforms()

def get_plataform_by_name(plataform_name: str, session: Session = Depends(get_session)):
    service = PlataformService(session)
    return service.get_plataform_by_name(plataform_name)

def update_plataform(plataform_id: str, plataform_update: PlataformUpdate, session: Session = Depends(get_session)):
    service = PlataformService(session)
    return service.update_plataform(plataform_id, plataform_update)

def delete_plataform(plataform_id: str, session: Session = Depends(get_session)):
    service = PlataformService(session)
    return service.delete_plataform(plataform_id)
