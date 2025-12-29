from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.rating import RatingService
from app.schemas.rating import RatingCreate
from app.utils.response import success_response

router = APIRouter()


@router.post("", response_model=None, status_code=201)
def create_rating(rating_data: RatingCreate, movie_id: int, db: Session = Depends(get_db)):
    service = RatingService(db)
    result = service.create_rating(movie_id, rating_data)
    return success_response(data=result.model_dump(), status_code=201)

