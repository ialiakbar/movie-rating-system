from typing import Optional, List
from pydantic import BaseModel, Field
from app.schemas.director import DirectorBase, DirectorDetail
from datetime import datetime


class MovieCreate(BaseModel):
    title: str
    director_id: int
    release_year: int
    cast: Optional[str] = None
    genres: List[int] = Field(default_factory=list)


class MovieUpdate(BaseModel):
    title: Optional[str] = None
    release_year: Optional[int] = None
    cast: Optional[str] = None
    genres: Optional[List[int]] = None


class MovieListItem(BaseModel):
    id: int
    title: str
    release_year: int
    director: DirectorBase
    genres: List[str]
    average_rating: Optional[float] = None
    ratings_count: int = 0


class MovieDetail(BaseModel):
    id: int
    title: str
    release_year: int
    cast: Optional[str] = None
    description: Optional[str] = None
    director: DirectorDetail
    genres: List[str]
    average_rating: Optional[float] = None
    ratings_count: int = 0


class PaginationMeta(BaseModel):
    page: int
    page_size: int
    total_items: int


class MovieListResponse(BaseModel):
    page: int
    page_size: int
    total_items: int
    items: List[MovieListItem]

