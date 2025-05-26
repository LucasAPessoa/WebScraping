from uuid import UUID, uuid4
from typing import List
from sqlmodel import Session, select
from app.models.models import Photo
from app.schemas.photo_schema import PhotoCreate, PhotoUpdate

class PhotoRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_photo(self, photo_create: PhotoCreate) -> Photo:
        photo = Photo(id=uuid4(), **photo_create.model_dump())
        self.session.add(photo)
        self.session.commit()
        self.session.refresh(photo)
        return photo

    def get_photo_by_id(self, photo_id: UUID) -> Photo | None:
        return self.session.get(Photo, photo_id)

    def get_all_photos(self) -> List[Photo]:
        return self.session.exec(select(Photo)).all()

    def update_photo(self, photo_id: UUID, photo_update: PhotoUpdate) -> Photo | None:
        photo = self.session.get(Photo, photo_id)
        if not photo:
            return None
        for key, value in photo_update.model_dump().items():
            setattr(photo, key, value)
        self.session.commit()
        self.session.refresh(photo)
        return photo

    def delete_photo(self, photo_id: UUID) -> None:
        photo = self.session.get(Photo, photo_id)
        if photo:
            self.session.delete(photo)
            self.session.commit()

    def get_photos_by_product_id(self, product_id: UUID) -> List[Photo]:
        return self.session.exec(
            select(Photo).where(Photo.product_id == product_id)
        ).all()