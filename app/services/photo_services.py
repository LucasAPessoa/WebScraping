from uuid import UUID
from fastapi import HTTPException
from sqlmodel import Session
import requests
from app.models.models import Photo
from app.models.models import Product_Placeholder
from app.repositories.photo_repository import PhotoRepository
from app.repositories.product_placeholder_repository import ProductPlaceholderRepository
from app.schemas.photo_schema import PhotoCreate, PhotoRead, PhotoUpdate, PhotoReadList

class PhotoService:
    def __init__(self, session: Session):
        self.photo_repository = PhotoRepository(session)
        self.product_placeholder_repository = ProductPlaceholderRepository(session)

    def create_photo(self, photo_create: PhotoCreate) -> PhotoRead:
        placeholder = self.product_placeholder_repository.get_by_id(photo_create.product_id)
        if not placeholder:
            raise HTTPException(status_code=404, detail="Produto não encontrado.")

        game_name = placeholder.name
        rawg_response = requests.get(
            f"https://api.rawg.io/api/games",
            params={"search": game_name, "key": "3d33178e180644ba9c0dcbaa98278664"}
        )

        if rawg_response.status_code != 200:
            raise HTTPException(status_code=502, detail="Erro ao consultar API do RAWG.")

        results = rawg_response.json().get("results")
        if not results:
            raise HTTPException(status_code=404, detail="Jogo não encontrado na RAWG.")

        background_image = results[0].get("background_image")
        if not background_image:
            raise HTTPException(status_code=404, detail="Imagem não encontrada.")

        new_photo = Photo(url=background_image, product_id=photo_create.product_id)
        return self.photo_repository.create_photo(new_photo)
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

    def get_photos_by_product_id(self, product_id: str) -> PhotoReadList:
        try:
            uuid = UUID(product_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="ID inválido.")

        photos = self.photo_repository.get_photos_by_product_id(uuid)
        if not photos:
            raise HTTPException(status_code=404, detail="Nenhuma foto encontrada para este produto.")
        return PhotoReadList(photos=[PhotoRead.model_validate(p) for p in photos])