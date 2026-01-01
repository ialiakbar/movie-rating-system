import logging
from typing import Optional
from fastapi import APIRouter, Depends, Query
from app.services.movie import MovieService
from app.services.dependencies import get_movie_service
from app.schemas.movie import MovieCreate, MovieUpdate
from app.utils.response import success_response, empty_response

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("", response_model=None)
def get_movies(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    title: Optional[str] = Query(None),
    release_year: Optional[int] = Query(None),
    genre: Optional[str] = Query(None),
    service: MovieService = Depends(get_movie_service),
):
    logger.info(f"Fetching movies list (route=/api/v1/movies, page={page}, page_size={page_size})")
    try:
        result = service.get_movie_list(page=page, page_size=page_size, title=title, release_year=release_year, genre=genre)
        return success_response(data=result.model_dump())
    except Exception as e:
        logger.error(f"Failed to fetch movies list (route=/api/v1/movies, page={page}, page_size={page_size})", exc_info=True)
        raise


@router.get("/{movie_id}", response_model=None)
def get_movie(movie_id: int, service: MovieService = Depends(get_movie_service)):
    result = service.get_movie_by_id(movie_id)
    return success_response(data=result.model_dump())


@router.post("", response_model=None, status_code=201)
def create_movie(movie_data: MovieCreate, service: MovieService = Depends(get_movie_service)):
    result = service.create_movie(movie_data)
    return success_response(data=result.model_dump(), status_code=201)


@router.put("/{movie_id}", response_model=None)
def update_movie(movie_id: int, movie_data: MovieUpdate, service: MovieService = Depends(get_movie_service)):
    result = service.update_movie(movie_id, movie_data)
    return success_response(data=result.model_dump())


@router.delete("/{movie_id}", response_model=None, status_code=204)
def delete_movie(movie_id: int, service: MovieService = Depends(get_movie_service)):
    service.delete_movie(movie_id)
    return empty_response()
