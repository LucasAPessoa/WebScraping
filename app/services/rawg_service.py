from typing import Optional, Dict, List, Any
import requests
from fastapi import HTTPException
import json
from datetime import datetime, timedelta
import os
import httpx

class RAWGService:
    def __init__(self):
        self.api_key = os.getenv("3d33178e180644ba9c0dcbaa98278664")
        self.base_url = "https://api.rawg.io/api"
        self.cache_dir = "cache/rawg"
        self.cache_duration = timedelta(days=1)
        
        # Criar diretório de cache se não existir
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)

    def _get_cache_path(self, game_name: str) -> str:
        return os.path.join(self.cache_dir, f"{game_name.lower().replace(' ', '_')}.json")

    def _is_cache_valid(self, cache_path: str) -> bool:
        if not os.path.exists(cache_path):
            return False
        
        cache_time = datetime.fromtimestamp(os.path.getmtime(cache_path))
        return datetime.now() - cache_time < self.cache_duration

    def _save_to_cache(self, game_name: str, data: Dict) -> None:
        cache_path = self._get_cache_path(game_name)
        with open(cache_path, 'w', encoding='utf-8') as f:
            json.dump(data, f)

    def _load_from_cache(self, game_name: str) -> Optional[Dict]:
        cache_path = self._get_cache_path(game_name)
        if self._is_cache_valid(cache_path):
            with open(cache_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None

    def search_game(self, game_name: str) -> Dict:
        # Verificar cache primeiro
        cached_data = self._load_from_cache(game_name)
        if cached_data:
            return cached_data

        # Fazer requisição à API
        response = requests.get(
            f"{self.base_url}/games",
            params={
                "search": game_name,
                "key": self.api_key,
                "page_size": 1
            }
        )

        if response.status_code != 200:
            raise HTTPException(
                status_code=502,
                detail="Erro ao buscar informações na RAWG API."
            )

        data = response.json()
        results = data.get("results", [])
        
        if not results:
            raise HTTPException(
                status_code=404,
                detail="Jogo não encontrado na RAWG API."
            )

        game_data = results[0]
        
        # Buscar detalhes adicionais do jogo
        game_id = game_data.get("id")
        if game_id:
            details = self._get_game_details(game_id)
            game_data.update(details)

        # Salvar no cache
        self._save_to_cache(game_name, game_data)
        
        return game_data

    def _get_game_details(self, game_id: int) -> Dict:
        response = requests.get(
            f"{self.base_url}/games/{game_id}",
            params={"key": self.api_key}
        )

        if response.status_code != 200:
            return {}

        return response.json()

    def get_metacritic_score(self, game_name: str) -> float:
        game_data = self.search_game(game_name)
        return float(game_data.get("metacritic", 0.0))

    def get_game_images(self, game_name: str) -> List[str]:
        game_data = self.search_game(game_name)
        images = []
        
        # Adicionar imagem de fundo
        if background_image := game_data.get("background_image"):
            images.append(background_image)
        
        # Adicionar screenshots
        if screenshots := game_data.get("short_screenshots", []):
            images.extend([screenshot.get("image") for screenshot in screenshots if screenshot.get("image")])
        
        return images

    def get_game_details(self, game_name: str) -> Dict:
        game_data = self.search_game(game_name)
        return {
            "name": game_data.get("name"),
            "description": game_data.get("description"),
            "metacritic_score": game_data.get("metacritic"),
            "released": game_data.get("released"),
            "rating": game_data.get("rating"),
            "rating_top": game_data.get("rating_top"),
            "platforms": [p.get("platform", {}).get("name") for p in game_data.get("platforms", [])],
            "genres": [g.get("name") for g in game_data.get("genres", [])],
            "developers": [d.get("name") for d in game_data.get("developers", [])],
            "publishers": [p.get("name") for p in game_data.get("publishers", [])],
            "background_image": game_data.get("background_image"),
            "website": game_data.get("website"),
            "background_image_additional": game_data.get("background_image_additional")
        }

    async def get_game_details(self, game_id: int) -> Optional[Dict[str, Any]]:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.base_url}/games/{game_id}",
                    params={"key": self.api_key}
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                print(f"Error fetching game details: {e}")
                return None

    async def search_games(self, query: str, page: int = 1, page_size: int = 20) -> Optional[Dict[str, Any]]:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.base_url}/games",
                    params={
                        "key": self.api_key,
                        "search": query,
                        "page": page,
                        "page_size": page_size
                    }
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                print(f"Error searching games: {e}")
                return None

    def format_game_data(self, game_data: Dict[str, Any]) -> Dict[str, Any]:
        """Format RAWG game data to match our schema"""
        return {
            "name": game_data.get("name", ""),
            "description": game_data.get("description", ""),
            "metacritic_score": game_data.get("metacritic", 0),
            "rating": game_data.get("rating", 0),
            "rating_top": game_data.get("rating_top", 5),
            "released_date": game_data.get("released"),
            "website": game_data.get("website"),
            "background_image": game_data.get("background_image"),
            "background_image_additional": game_data.get("background_image_additional"),
            "genres": [genre["name"] for genre in game_data.get("genres", [])],
            "developers": [dev["name"] for dev in game_data.get("developers", [])],
            "publishers": [pub["name"] for pub in game_data.get("publishers", [])]
        } 