import logging
from sqlalchemy.orm import Session
from app.repositories.movie_rating import MovieRatingRepository
from app.repositories.movie import MovieRepository
from app.schemas.rating import RatingCreate, RatingResponse
from app.exceptions.movie import MovieNotFoundError
from app.exceptions.rating import InvalidRatingScoreError

logger = logging.getLogger(__name__)


class RatingService:
    def __init__(self, db: Session, rating_repo: MovieRatingRepository, movie_repo: MovieRepository):
        self.db = db
        self.rating_repo = rating_repo
        self.movie_repo = movie_repo

    def create_rating(self, movie_id: int, rating_data: RatingCreate) -> RatingResponse:
        movie = self.movie_repo.get_by_id(movie_id)
        if not movie:
            raise MovieNotFoundError(movie_id)

        if not (1 <= rating_data.score <= 10):
            logger.warning(f"Invalid rating value (movie_id={movie_id}, rating={rating_data.score}, route=/api/v1/movies/{movie_id}/ratings)")
            raise InvalidRatingScoreError(rating_data.score)

        rating = self.rating_repo.create(movie_id=movie_id, score=rating_data.score)
        logger.info(f"Rating saved successfully (movie_id={movie_id}, rating={rating_data.score})")

        return RatingResponse(rating_id=rating.id, movie_id=rating.movie_id, score=rating.score, created_at=rating.rated_at)
