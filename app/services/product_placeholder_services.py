from fastapi import HTTPException
from app.repositories.product_placeholder_repository import ProductPlaceholderRepository
from app.repositories.promotion_repository import PromotionRepository
from app.schemas.product_placeholder_schema import ProductPlaceholderCreate, ProductPlaceholderUpdate, ProductPlaceholderRead, ProductPlaceholderReadList, ProductPlaceholderUpdateFields
from app.schemas.rawg_schema import RAWGSearchResult, RAWGGame, RAWGScreenshotsResult, RAWGScreenshot, RAWGParams
from typing import List, Optional
import requests
import json
from uuid import uuid4
from datetime import datetime, timedelta
import os
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class ProductPlaceholderService:
    def __init__(self, repository: ProductPlaceholderRepository, promotion_repository: PromotionRepository):
        self.repository = repository
        self.promotion_repository = promotion_repository
        self.rawg_api_key = os.getenv("RAWG_API_KEY", "3d33178e180644ba9c0dcbaa98278664")
        self.rawg_base_url = "https://api.rawg.io/api"

    def _fetch_rawg_data(self, endpoint: str, params: RAWGParams) -> RAWGSearchResult | RAWGGame | RAWGScreenshotsResult:
        """Método genérico para fazer requisições à RAWG API"""
        url = f"{self.rawg_base_url}/{endpoint}"
        params_dict = params.model_dump(exclude_unset=True)
        params_dict["key"] = self.rawg_api_key
        
        try:
            logger.debug(f"Requesting RAWG API: {endpoint}")
            response = requests.get(url, params=params_dict)
            response.raise_for_status()
            data = response.json()
            
            if not data:
                raise HTTPException(status_code=404, detail="Dados não encontrados na RAWG API")
            
            if "results" in data:
                if "image" in data["results"][0]:
                    return RAWGScreenshotsResult.model_validate(data)
                return RAWGSearchResult.model_validate(data)
            return RAWGGame.model_validate(data)
            
        except requests.exceptions.RequestException as e:
            if e.response and e.response.status_code == 404:
                raise HTTPException(status_code=404, detail="Dados não encontrados na RAWG API")
            raise HTTPException(status_code=500, detail=f"Erro na RAWG API: {str(e)}")
        except json.JSONDecodeError:
            raise HTTPException(status_code=500, detail="Erro ao decodificar resposta da RAWG API")

    def _search_game(self, game_name: str) -> RAWGGame:
        """Busca um jogo na RAWG API"""
        if not game_name or not isinstance(game_name, str):
            raise HTTPException(status_code=400, detail="Nome do jogo inválido")

        try:
            logger.debug(f"Searching for game: {game_name}")
            data = self._fetch_rawg_data("games", RAWGParams(search=game_name, page_size=5))
            
            if not isinstance(data, RAWGSearchResult) or not data.results:
                raise HTTPException(status_code=404, detail=f"Jogo '{game_name}' não encontrado na RAWG API")
            
            # Procura por uma correspondência exata do nome
            for game in data.results:
                if game.name.lower() == game_name.lower():
                    logger.debug(f"Found exact match: {game.name}")
                    return game
            
            # Se não encontrar correspondência exata, retorna o primeiro resultado
            first_result = data.results[0]
            if not first_result:
                raise HTTPException(status_code=500, detail="Resposta inválida da RAWG API")
            
            logger.debug(f"Using first result: {first_result.name}")
            return first_result
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error searching game: {str(e)}", exc_info=True)
            raise HTTPException(status_code=500, detail=f"Erro ao buscar jogo: {str(e)}")

    def _get_game_details(self, game_id: int) -> RAWGGame:
        """Obtém detalhes completos do jogo"""
        return self._fetch_rawg_data(f"games/{game_id}", RAWGParams())

    def _get_game_screenshots(self, game_id: int) -> List[RAWGScreenshot]:
        """Obtém screenshots do jogo"""
        data = self._fetch_rawg_data(f"games/{game_id}/screenshots", RAWGParams())
        logger.debug(f"Screenshots data type: {type(data)}")
        logger.debug(f"Screenshots data: {data}")
        if isinstance(data, RAWGScreenshotsResult):
            logger.debug(f"Number of screenshots found: {len(data.results)}")
            for screenshot in data.results:
                logger.debug(f"Screenshot URL: {screenshot.image}")
            return data.results
        logger.warning("No screenshots found or invalid response format")
        return []

    def _format_game_data(self, game_data: RAWGGame, screenshots: List[RAWGScreenshot]) -> ProductPlaceholderUpdateFields:
        """Formata os dados do jogo para o formato do nosso modelo"""
        try:
            logger.debug("Starting to format game data")
            logger.debug(f"Number of screenshots to process: {len(screenshots)}")
            screenshot_urls = [s.image for s in screenshots]
            logger.debug(f"Screenshot URLs: {screenshot_urls}")
            
            formatted_data = ProductPlaceholderUpdateFields(
                name=game_data.name,
                description=game_data.description,
                metacritic_score=game_data.metacritic,
                rating=game_data.rating,
                released=game_data.released,
                background_image=game_data.background_image,
                background_image_additional=game_data.background_image_additional,
                website=game_data.website,
                rawg_id=game_data.id,
                genres=", ".join(genre.get("name", "") for genre in game_data.genres),
                platforms=", ".join(
                    f"{p.platform.get('name', '')} "
                    f"{('Min: ' + p.requirements.get('minimum', '') if p.requirements and p.requirements.get('minimum') else '')} "
                    f"{('Rec: ' + p.requirements.get('recommended', '') if p.requirements and p.requirements.get('recommended') else '')}"
                    for p in game_data.platforms
                ),
                developers=", ".join(dev.get("name", "") for dev in game_data.developers),
                publishers=", ".join(pub.get("name", "") for pub in game_data.publishers),
                screenshots=screenshot_urls,
                esrb_rating=game_data.esrb_rating.get("name") if game_data.esrb_rating else None,
                playtime=game_data.playtime,
                achievements_count=game_data.achievements_count,
                parent_platforms=", ".join(p.get("platform", {}).get("name", "") for p in game_data.parent_platforms)
            )
            logger.debug("Successfully formatted game data")
            return formatted_data
        except Exception as e:
            logger.error(f"Error formatting game data: {str(e)}", exc_info=True)
            raise HTTPException(status_code=500, detail=f"Erro ao formatar dados do jogo: {str(e)}")

    def _create_launch_promotion(self, product_name: str) -> str:
        """Cria uma promoção de lançamento para o produto"""
        promotion_data = {
            "id": str(uuid4()),
            "name": f"Promoção de Lançamento - {product_name}",
            "description": f"Promoção especial de lançamento para {product_name}",
            "start_date": datetime.now(),
            "end_date": datetime.now() + timedelta(days=7),
            "is_active": True,
            "discount_percentage": 10.0
        }
        
        promotion = self.promotion_repository.create_promotion(promotion_data)
        return promotion.id

    def _format_product_data(self, name: str) -> ProductPlaceholderUpdateFields:
        """Formata os dados do produto baseado no nome"""
        # Busca e processa dados do jogo com o nome
        game = self._search_game(name)
        game_details = self._get_game_details(game.id)
        screenshots = self._get_game_screenshots(game.id)
        return self._format_game_data(game_details, screenshots)

    def create_product_placeholder(self, product_data: ProductPlaceholderCreate) -> ProductPlaceholderRead:
        """Cria um novo produto placeholder"""
        try:
            
            
            
            logger.debug("Starting product creation process")
            # Primeiro busca e processa dados do jogo na RAWG API
            game = self._search_game(product_data.name)
            game_details = self._get_game_details(game.id)
            screenshots = self._get_game_screenshots(game.id)
            formatted_data = self._format_game_data(game_details, screenshots)
            logger.debug("Game data formatted successfully")

            # Verifica se o produto já existe no banco
            logger.debug("Checking for existing products")
            existing_products = self.repository.get_all_product_placeholder()
            for product in existing_products:
                if product.name.lower().strip().replace(":", "") == product_data.name.lower().strip().replace(":", ""):
                    raise Exception("Produto já existe")
            logger.debug("No existing product found")

            # Cria o produto com ID gerado
            logger.debug("Creating new product")
            product_id = str(uuid4())
            formatted_data.id = product_id
            logger.debug(f"Generated product ID: {product_id}")
            
            try:
                product = self.repository.create_product_placeholder(formatted_data)
                logger.debug("Product created successfully in repository")
            except Exception as e:
                logger.error(f"Error creating product in repository: {str(e)}", exc_info=True)
                raise

            logger.debug("Converting product to read model")
            return ProductPlaceholderRead.model_validate(product)

        except Exception as e:
            logger.error(f"Error in create_product_placeholder: {str(e)}", exc_info=True)
            raise HTTPException(status_code=500, detail=str(e))

    def get_all_product_placeholder(self) -> List[ProductPlaceholderRead]:
        """Retorna todos os produtos placeholder"""
        products = self.repository.get_all_product_placeholder()
        return [ProductPlaceholderRead.model_validate(product) for product in products]

    def get_product_placeholder_by_id(self, product_id: str) -> Optional[ProductPlaceholderRead]:
        """Busca um produto placeholder pelo ID"""
        product = self.repository.get_product_placeholder_by_id(product_id)
        if not product:
            return None
        return ProductPlaceholderRead.model_validate(product)

    def update_product_placeholder(self, product_id: str, product_data: ProductPlaceholderUpdate) -> Optional[ProductPlaceholderRead]:
        """Atualiza um produto placeholder"""
        try:
            # Verifica se o produto já existe no banco
            existing_products = self.repository.get_all_product_placeholder()
            for product in existing_products:
                if product.name.lower().strip().replace(":", "") == product_data.name.lower().strip().replace(":", ""):
                    raise Exception("Produto já existe")
            
            # Busca e processa dados do jogo com o novo nome
            game = self._search_game(product_data.name)
            game_details = self._get_game_details(game.id)
            screenshots = self._get_game_screenshots(game.id)
            formatted_data = self._format_game_data(game_details, screenshots)

            new_product_data = ProductPlaceholderUpdateFields(**formatted_data.model_dump())
            new_product_data.id = product_id
            
            logger.debug(f"Product data: {product_data}")

            # Atualiza o produto com todos os dados usando o repository
            product = self.repository.update_product_placeholder(product_id, new_product_data)
            if not product:
                return None

            return ProductPlaceholderRead.model_validate(product)

        except Exception as e:
            self.repository.db.rollback()
            raise HTTPException(status_code=500, detail=str(e))

    def delete_product_placeholder(self, product_id: str) -> bool:
        """Remove um produto placeholder"""
        return self.repository.delete_product_placeholder(product_id)
