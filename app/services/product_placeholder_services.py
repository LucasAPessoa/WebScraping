import requests
from uuid import UUID
from fastapi import HTTPException
from sqlmodel import Session

from app.repositories.photo_repository import PhotoRepository
from app.repositories.product_placeholder_repository import ProductPlaceholderRepository
from app.schemas.photo_schema import PhotoCreate
from app.schemas.product_placeholder_schema import (
    ProductPlaceholderCreate,
    ProductPlaceholderRead,
    ProductPlaceholderUpdate,
    ProductPlaceholderReadList
)

class ProductPlaceholderService:
    def __init__(self, session: Session):
        self.repository = ProductPlaceholderRepository(session)
        self.photo_repository = PhotoRepository(session)

    def fetch_metacritic_score(self, game_name: str) -> float:
        response = requests.get(f"https://api.rawg.io/api/games", params={
            "search": game_name,
            "key": "3d33178e180644ba9c0dcbaa98278664"
        })

        if response.status_code != 200:
            raise HTTPException(status_code=502, detail="Erro ao buscar metacritic na API externa.")

        data = response.json()
        results = data.get("results")
        if not results:
            raise HTTPException(status_code=404, detail="Jogo não encontrado na API externa.")

        return float(results[0].get("metacritic", 0.0))  # Pode ajustar conforme estrutura da API

    def fetch_photos_from_rawg(self, game_name: str) -> list[str]:
        response = requests.get(f"https://api.rawg.io/api/games", params={
            "search": game_name,
            "key": "3d33178e180644ba9c0dcbaa98278664"
        })

        if response.status_code != 200:
            return []

        data = response.json()
        results = data.get("results", [])
        images = []
        for result in results:
            bg_image = result.get("background_image")
            if bg_image:
                images.append(bg_image)

        return images

    def create_product_placeholder(self, data: ProductPlaceholderCreate) -> ProductPlaceholderRead:
        score = self.fetch_metacritic_score(data.name)
        product = self.repository.create_product_placeholder(data, score)

        image_urls = self.fetch_photos_from_rawg(data.name)
        for url in image_urls:
            photo_data = PhotoCreate(url=url, product_placeholder_id=product.id)
            self.photo_repository.create_photo(photo_data)

        return ProductPlaceholderRead.model_validate(product)

    def get_all_product_placeholder(self) -> ProductPlaceholderReadList:
        products = self.repository.get_all_product_placeholer()
        return ProductPlaceholderReadList(products=[ProductPlaceholderRead.model_validate(p) for p in products])

    def get_product_placeholder_by_id(self, product_id: str) -> ProductPlaceholderRead:
        try:
            uuid = UUID(product_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="ID inválido.")

        product = self.repository.get__product_placeholer_by_id(uuid)
        if not product:
            raise HTTPException(status_code=404, detail="Produto não encontrado.")

        return ProductPlaceholderRead.model_validate(product)

    def update_product_placeholder(self, product_id: str, data: ProductPlaceholderUpdate) -> ProductPlaceholderRead:
        try:
            uuid = UUID(product_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="ID inválido.")

        score = self.fetch_metacritic_score(data.name)
        updated = self.repository.update_product_placeholer(uuid, data, score)

        if not updated:
            raise HTTPException(status_code=404, detail="Produto não encontrado.")

        return ProductPlaceholderRead.model_validate(updated)

    def delete_product_placeholder(self, product_id: str):
        try:
            uuid = UUID(product_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="ID inválido.")

        self.repository.delete_product_placeholer(uuid)
