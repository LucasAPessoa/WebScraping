from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from datetime import datetime
import json

class ProductPlaceholderCreate(BaseModel):
    name: str = Field(..., description="Nome do jogo")

class ProductPlaceholderUpdate(BaseModel):
    name: str = Field(..., description="Nome do jogo")

class ProductPlaceholderUpdateFields(BaseModel):
    id: Optional[str] = Field(None, description="ID único do produto placeholder")
    name: str = Field(..., description="Nome do jogo")
    description: Optional[str] = Field(None, description="Descrição do jogo")
    metacritic_score: Optional[int] = Field(None, description="Pontuação no Metacritic")
    rating: Optional[float] = Field(None, description="Avaliação geral")
    released: Optional[str] = Field(None, description="Data de lançamento")
    background_image: Optional[str] = Field(None, description="URL da imagem de fundo")
    background_image_additional: Optional[str] = Field(None, description="URL da imagem adicional")
    website: Optional[str] = Field(None, description="Website oficial")
    rawg_id: Optional[int] = Field(None, description="ID do jogo na RAWG API")
    genres: Optional[str] = Field(None, description="Gêneros do jogo")
    platforms: Optional[str] = Field(None, description="Plataformas disponíveis")
    developers: Optional[str] = Field(None, description="Desenvolvedores")
    publishers: Optional[str] = Field(None, description="Publicadores")
    screenshots: Optional[List[str]] = Field(None, description="Lista de URLs das screenshots")
    esrb_rating: Optional[str] = Field(None, description="Classificação ESRB")
    playtime: Optional[int] = Field(None, description="Tempo de jogo estimado")
    achievements_count: Optional[int] = Field(None, description="Número de conquistas")
    parent_platforms: Optional[str] = Field(None, description="Plataformas principais")
        
    model_config = {
        "from_attributes": True
    }
        
    @field_validator('screenshots', mode='before')
    @classmethod
    def parse_screenshots(cls, v):
        if v is None:
            return []
        if isinstance(v, str):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return []
        if isinstance(v, list):
            return v
        return []
    
    def model_dump(self, **kwargs):
        data = super().model_dump(**kwargs)
        if 'screenshots' in data and data['screenshots'] is not None:
            data['screenshots'] = json.dumps(data['screenshots'])
        return data
    
class ProductPlaceholderRead(BaseModel):
    id: str = Field(..., description="ID único do produto placeholder")
    name: str = Field(..., description="Nome do jogo")
    description: Optional[str] = Field(None, description="Descrição do jogo")
    metacritic_score: Optional[int] = Field(None, description="Pontuação no Metacritic")
    rating: Optional[float] = Field(None, description="Avaliação geral")
    released: Optional[str] = Field(None, description="Data de lançamento")
    background_image: Optional[str] = Field(None, description="URL da imagem de fundo")
    background_image_additional: Optional[str] = Field(None, description="URL da imagem adicional")
    website: Optional[str] = Field(None, description="Website oficial")
    rawg_id: Optional[int] = Field(None, description="ID do jogo na RAWG API")
    genres: Optional[str] = Field(None, description="Gêneros do jogo")
    platforms: Optional[str] = Field(None, description="Plataformas disponíveis")
    developers: Optional[str] = Field(None, description="Desenvolvedores")
    publishers: Optional[str] = Field(None, description="Publicadores")
    screenshots: Optional[List[str]] = Field(None, description="Lista de URLs das screenshots")
    esrb_rating: Optional[str] = Field(None, description="Classificação ESRB")
    playtime: Optional[int] = Field(None, description="Tempo de jogo estimado")
    achievements_count: Optional[int] = Field(None, description="Número de conquistas")
    parent_platforms: Optional[str] = Field(None, description="Plataformas principais")

    model_config = {
        "from_attributes": True
    }

    @field_validator('screenshots', mode='before')
    @classmethod
    def parse_screenshots(cls, v):
        if v is None:
            return []
        if isinstance(v, str):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return []
        if isinstance(v, list):
            return v
        return []

class ProductPlaceholderReadList(BaseModel):
    id: str = Field(..., description="ID único do produto placeholder")
    name: str = Field(..., description="Nome do jogo")
    description: Optional[str] = Field(None, description="Descrição do jogo")
    metacritic_score: Optional[int] = Field(None, description="Pontuação no Metacritic")
    rating: Optional[float] = Field(None, description="Avaliação geral")
    released: Optional[str] = Field(None, description="Data de lançamento")
    background_image: Optional[str] = Field(None, description="URL da imagem de fundo")
    background_image_additional: Optional[str] = Field(None, description="URL da imagem adicional")
    website: Optional[str] = Field(None, description="Website oficial")
    rawg_id: Optional[int] = Field(None, description="ID do jogo na RAWG API")
    genres: Optional[str] = Field(None, description="Gêneros do jogo")
    platforms: Optional[str] = Field(None, description="Plataformas disponíveis")
    developers: Optional[str] = Field(None, description="Desenvolvedores")
    publishers: Optional[str] = Field(None, description="Publicadores")
    screenshots: Optional[List[str]] = Field(None, description="Lista de URLs das screenshots")
    esrb_rating: Optional[str] = Field(None, description="Classificação ESRB")
    playtime: Optional[int] = Field(None, description="Tempo de jogo estimado")
    achievements_count: Optional[int] = Field(None, description="Número de conquistas")
    parent_platforms: Optional[str] = Field(None, description="Plataformas principais")

    model_config = {
        "from_attributes": True
    }

    @field_validator('screenshots', mode='before')
    @classmethod
    def parse_screenshots(cls, v):
        if v is None:
            return []
        if isinstance(v, str):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return []
        if isinstance(v, list):
            return v
        return []

class ProductPlaceholderDelete(BaseModel):
    message: str = Field(..., description="Placeholder deletado com sucesso")

