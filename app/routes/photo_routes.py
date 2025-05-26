from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from app.controllers import photo_controller
from app.schemas.photo_schema import PhotoCreate, PhotoRead, PhotoUpdate, PhotoReadList
from app.database.session import get_session

photo_router = APIRouter(prefix="/photos", tags=["Photos"])

@photo_router.post("/", response_model=PhotoRead, status_code=status.HTTP_201_CREATED)
def create_photo(photo_create: PhotoCreate, session: Session = Depends(get_session)):
    return photo_controller.create_photo(photo_create, session)

@photo_router.get("/{photo_id}", response_model=PhotoRead, status_code=status.HTTP_200_OK)
def get_photo_by_id(photo_id: str, session: Session = Depends(get_session)):
    return photo_controller.get_photo_by_id(photo_id, session)

@photo_router.get("/", response_model=PhotoReadList, status_code=status.HTTP_200_OK)
def get_all_photos(session: Session = Depends(get_session)):
    return photo_controller.get_all_photos(session)

@photo_router.put("/{photo_id}", response_model=PhotoRead, status_code=status.HTTP_200_OK)
def update_photo(photo_id: str, photo_update: PhotoUpdate, session: Session = Depends(get_session)):
    return photo_controller.update_photo(photo_id, photo_update, session)

@photo_router.delete("/{photo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_photo(photo_id: str, session: Session = Depends(get_session)):
    return photo_controller.delete_photo(photo_id, session)

@photo_router.get("/product/{product_id}", response_model=PhotoReadList, status_code=status.HTTP_200_OK)
def get_photos_by_product_id(product_id: str, session: Session = Depends(get_session)):
    return photo_controller.get_photos_by_product_id(product_id, session)
