from typing import Optional
from sqlalchemy.orm import Session
from app.models.movie_rating import MovieRating


class MovieRatingRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, movie_id: int, score: int) -> MovieRating:
        rating = MovieRating(movie_id=movie_id, score=score)
        self.db.add(rating)
        self.db.commit()
        self.db.refresh(rating)
        return rating

    def get_by_id(self, rating_id: int) -> Optional[MovieRating]:
        return self.db.query(MovieRating).filter(MovieRating.id == rating_id).first()

    def get_by_movie_id(self, movie_id: int) -> list[MovieRating]:
        return self.db.query(MovieRating).filter(MovieRating.movie_id == movie_id).all()

