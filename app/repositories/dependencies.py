from sqlalchemy.orm import Session
from app.repositories.director import DirectorRepository
from app.repositories.genre import GenreRepository
from app.repositories.movie import MovieRepository
from app.repositories.movie_rating import MovieRatingRepository


def get_director_repository(db: Session) -> DirectorRepository:
    return DirectorRepository(db)


def get_genre_repository(db: Session) -> GenreRepository:
    return GenreRepository(db)


def get_movie_repository(db: Session) -> MovieRepository:
    return MovieRepository(db)


def get_rating_repository(db: Session) -> MovieRatingRepository:
    return MovieRatingRepository(db)

