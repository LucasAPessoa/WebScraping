import requests
from uuid import UUID
from fastapi import HTTPException
from sqlmodel import Session
import json
from typing import Dict, List, Optional

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
        self.rawg_api_key = "3d33178e180644ba9c0dcbaa98278664"

    def fetch_game_data(self, game_name: str) -> Dict:
        """Busca dados do jogo na RAWG API"""
        response = requests.get(
            f"https://api.rawg.io/api/games",
            params={
                "search": game_name,
                "key": self.rawg_api_key,
                "page_size": 1
            }
        )

        if response.status_code != 200:
            raise HTTPException(status_code=502, detail="Erro ao buscar informações na RAWG API.")

        data = response.json()
        results = data.get("results", [])
        
        if not results:
            raise HTTPException(status_code=404, detail="Jogo não encontrado na RAWG API.")

        game_data = results[0]
        
        # Buscar detalhes adicionais do jogo
        game_id = game_data.get("id")
        if game_id:
            details = self._get_game_details(game_id)
            game_data.update(details)

        return game_data

    def _get_game_details(self, game_id: int) -> Dict:
        """Busca detalhes adicionais do jogo"""
        response = requests.get(
            f"https://api.rawg.io/api/games/{game_id}",
            params={"key": self.rawg_api_key}
        )

        if response.status_code != 200:
            return {}

        return response.json()

    def _extract_game_info(self, game_data: Dict) -> Dict:
        """Extrai informações relevantes do jogo da resposta da API."""
        metacritic = game_data.get("metacritic")
        return {
            "metacritic_score": float(metacritic) if metacritic is not None else 0.0,
            "rating": float(game_data.get("rating", 0.0)),
            "rating_top": int(game_data.get("rating_top", 0)),
            "released_date": game_data.get("released", ""),
            "website": game_data.get("website", ""),
            "background_image": game_data.get("background_image", ""),
            "background_image_additional": game_data.get("background_image_additional", ""),
            "genres": [genre["name"] for genre in game_data.get("genres", [])],
            "developers": [dev["name"] for dev in game_data.get("developers", [])],
            "publishers": [pub["name"] for pub in game_data.get("publishers", [])]
        }

    def _get_game_images(self, game_data: Dict) -> List[str]:
        """Extrai URLs das imagens do jogo"""
        images = []
        
        # Adicionar imagem de fundo
        if background_image := game_data.get("background_image"):
            images.append(background_image)
        
        # Adicionar screenshots
        if screenshots := game_data.get("short_screenshots", []):
            images.extend([screenshot.get("image") for screenshot in screenshots if screenshot.get("image")])
        
        return images

    def create_product_placeholder(self, data: ProductPlaceholderCreate) -> ProductPlaceholderRead:
        # Buscar dados do jogo
        game_data = self.fetch_game_data(data.name)
        game_info = self._extract_game_info(game_data)
        
        # Criar o produto com todas as informações
        product = self.repository.create_product_placeholder(data, **game_info)

        # Salvar as imagens
        images = self._get_game_images(game_data)
        for url in images:
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

        product = self.repository.get_product_placeholder_by_id(uuid)
        if not product:
            raise HTTPException(status_code=404, detail="Produto não encontrado.")

        return ProductPlaceholderRead.model_validate(product)

    def update_product_placeholder(self, product_id: str, data: ProductPlaceholderUpdate) -> ProductPlaceholderRead:
        try:
            uuid = UUID(product_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="ID inválido.")

        # Buscar dados atualizados do jogo
        game_data = self.fetch_game_data(data.name)
        game_info = self._extract_game_info(game_data)
        
        # Atualizar o produto
        updated = self.repository.update_product_placeholer(uuid, data, **game_info)

        if not updated:
            raise HTTPException(status_code=404, detail="Produto não encontrado.")

        # Atualizar as imagens
        images = self._get_game_images(game_data)
        for url in images:
            photo_data = PhotoCreate(url=url, product_placeholder_id=uuid)
            self.photo_repository.create_photo(photo_data)

        return ProductPlaceholderRead.model_validate(updated)

    def delete_product_placeholder(self, product_id: str):
        try:
            uuid = UUID(product_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="ID inválido.")

        self.repository.delete_product_placeholer(uuid)
