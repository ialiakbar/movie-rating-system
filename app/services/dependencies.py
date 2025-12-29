from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.repositories.dependencies import (
    get_director_repository,
    get_genre_repository,
    get_movie_repository,
    get_rating_repository,
)
from app.services.movie import MovieService
from app.services.rating import RatingService


def get_movie_service(db: Session = Depends(get_db)) -> MovieService:
    """Create MovieService with all repositories using the same db session."""
    director_repo = get_director_repository(db)
    genre_repo = get_genre_repository(db)
    movie_repo = get_movie_repository(db)
    return MovieService(db=db, director_repo=director_repo, genre_repo=genre_repo, movie_repo=movie_repo)


def get_rating_service(db: Session = Depends(get_db)) -> RatingService:
    """Create RatingService with all repositories using the same db session."""
    rating_repo = get_rating_repository(db)
    movie_repo = get_movie_repository(db)
    return RatingService(db=db, rating_repo=rating_repo, movie_repo=movie_repo)

