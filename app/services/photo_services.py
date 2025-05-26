from uuid import UUID
from fastapi import HTTPException
from sqlmodel import Session
from app.repositories.photo_repository import PhotoRepository
from app.schemas.photo_schema import PhotoCreate, PhotoRead, PhotoUpdate, PhotoReadList

class PhotoService:
    def __init__(self, session: Session):
        self.photo_repository = PhotoRepository(session)

    def create_photo(self, photo_create: PhotoCreate) -> PhotoRead:
        if not photo_create.url.strip():
            raise HTTPException(status_code=400, detail="URL da foto é obrigatória.")
        
        photo_create.product_id
        return self.photo_repository.create_photo(photo_create)

    def get_photo_by_id(self, photo_id: str) -> PhotoRead:
        try:
            uuid = UUID(photo_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="ID inválido.")

        photo = self.photo_repository.get_photo_by_id(uuid)
        if not photo:
            raise HTTPException(status_code=404, detail="Foto não encontrada.")
        return photo

    def get_all_photos(self) -> PhotoReadList:
        photos = self.photo_repository.get_all_photos()
        if not photos:
            raise HTTPException(status_code=404, detail="Nenhuma foto encontrada.")
        return PhotoReadList(photos=[PhotoRead.model_validate(p) for p in photos])

    def update_photo(self, photo_id: str, photo_update: PhotoUpdate) -> PhotoRead:
        try:
            uuid = UUID(photo_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="ID inválido.")

        photo = self.photo_repository.update_photo(uuid, photo_update)
        if not photo:
            raise HTTPException(status_code=404, detail="Foto não encontrada.")
        return photo

    def delete_photo(self, photo_id: str) -> None:
        try:
            uuid = UUID(photo_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="ID inválido.")

        photo = self.photo_repository.get_photo_by_id(uuid)
        if not photo:
            raise HTTPException(status_code=404, detail="Foto não encontrada.")

        self.photo_repository.delete_photo(uuid)
