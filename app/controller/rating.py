import logging
from fastapi import APIRouter, Depends
from app.services.rating import RatingService
from app.services.dependencies import get_rating_service
from app.schemas.rating import RatingCreate
from app.utils.response import success_response

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("", response_model=None, status_code=201)
def create_rating(rating_data: RatingCreate, movie_id: int, service: RatingService = Depends(get_rating_service)):
    logger.info(f"Rating movie (movie_id={movie_id}, rating={rating_data.score}, route=/api/v1/movies/{movie_id}/ratings)")
    result = service.create_rating(movie_id, rating_data)
    return success_response(data=result.model_dump(), status_code=201)
