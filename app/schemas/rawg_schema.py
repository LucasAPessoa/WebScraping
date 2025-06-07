from pydantic import BaseModel, Field
from typing import List, Optional, Any, Dict

class RAWGPlatform(BaseModel):
    platform: dict
    requirements: Optional[dict] = None

class RAWGGame(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    metacritic: Optional[int] = None
    rating: Optional[float] = None
    released: Optional[str] = None
    background_image: Optional[str] = None
    background_image_additional: Optional[str] = None
    website: Optional[str] = None
    genres: List[dict] = []
    platforms: List[RAWGPlatform] = []
    developers: List[dict] = []
    publishers: List[dict] = []
    esrb_rating: Optional[dict] = None
    playtime: Optional[int] = None
    achievements_count: Optional[int] = None
    parent_platforms: List[dict] = []

class RAWGSearchResult(BaseModel):
    count: int
    next: Optional[str] = None
    previous: Optional[str] = None
    results: List[RAWGGame]

class RAWGScreenshot(BaseModel):
    id: int
    image: str
    width: int
    height: int
    is_deleted: bool

class RAWGScreenshotsResult(BaseModel):
    count: int
    next: Optional[str] = None
    previous: Optional[str] = None
    results: List[RAWGScreenshot]

class RAWGParams(BaseModel):
    search: Optional[str] = None
    page_size: Optional[int] = None
    key: Optional[str] = None
    # Add any other parameters that might be needed for RAWG API calls