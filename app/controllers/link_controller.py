from fastapi import Depends
from sqlmodel import Session
from app.schemas.link_schema import LinkCreate, LinkUpdate
from app.services.link_services import LinkService
from app.database.session import get_session

def create_link(link_create: LinkCreate, session: Session = Depends(get_session)):
    service = LinkService(session)
    return service.create_link(link_create)

def get_link_by_id(link_id: str, session: Session = Depends(get_session)):
    service = LinkService(session)
    return service.get_link_by_id(link_id)

def get_all_links(session: Session = Depends(get_session)):
    service = LinkService(session)
    return service.get_all_links()

def get_link_by_name(link_name: str, session: Session = Depends(get_session)):
    service = LinkService(session)
    return service.get_link_by_name(link_name)

def update_link(link_id: str, link_update: LinkUpdate, session: Session = Depends(get_session)):
    service = LinkService(session)
    return service.update_link(link_id, link_update)

def delete_link(link_id: str, session: Session = Depends(get_session)):
    service = LinkService(session)
    return service.delete_link(link_id)