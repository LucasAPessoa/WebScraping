from fastapi import Depends
from sqlmodel import Session
from app.schemas.photo_schema import PhotoCreate, PhotoUpdate
from app.services.photo_services import PhotoService
from app.database.session import get_session

def create_photo(photo_create: PhotoCreate, session: Session = Depends(get_session)):
    service = PhotoService(session)
    return service.create_photo(photo_create)

def get_photo_by_id(photo_id: str, session: Session = Depends(get_session)):
    service = PhotoService(session)
    return service.get_photo_by_id(photo_id)

def get_all_photos(session: Session = Depends(get_session)):
    service = PhotoService(session)
    return service.get_all_photos()

def update_photo(photo_id: str, photo_update: PhotoUpdate, session: Session = Depends(get_session)):
    service = PhotoService(session)
    return service.update_photo(photo_id, photo_update)

def delete_photo(photo_id: str, session: Session = Depends(get_session)):
    service = PhotoService(session)
    return service.delete_photo(photo_id)

def get_photos_by_product_id(product_id: str, session: Session = Depends(get_session)):
    service = PhotoService(session)
    return service.get_photos_by_product_id(product_id)