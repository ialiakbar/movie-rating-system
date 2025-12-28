from typing import Optional
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from app.models.movie import Movie
from app.models.genre import Genre
from app.models.movie_rating import MovieRating


class MovieRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, movie_id: int) -> Optional[Movie]:
        return (
            self.db.query(Movie)
            .options(joinedload(Movie.director), joinedload(Movie.genres))
            .filter(Movie.id == movie_id)
            .first()
        )

    def create(
        self, title: str, director_id: int, release_year: int, cast: Optional[str] = None, description: Optional[str] = None, genre_ids: Optional[list[int]] = None
    ) -> Movie:
        movie = Movie(title=title, director_id=director_id, release_year=release_year, cast=cast, description=description)
        if genre_ids:
            genres = self.db.query(Genre).filter(Genre.id.in_(genre_ids)).all()
            movie.genres = genres
        self.db.add(movie)
        self.db.commit()
        self.db.refresh(movie)
        return movie

    def update(self, movie: Movie, **kwargs) -> Movie:
        for key, value in kwargs.items():
            if value is not None:
                setattr(movie, key, value)
        self.db.commit()
        self.db.refresh(movie)
        return movie

    def update_genres(self, movie: Movie, genre_ids: list[int]) -> Movie:
        genres = self.db.query(Genre).filter(Genre.id.in_(genre_ids)).all()
        movie.genres = genres
        self.db.commit()
        self.db.refresh(movie)
        return movie

    def delete(self, movie: Movie) -> None:
        self.db.delete(movie)
        self.db.commit()

    def get_list(
        self,
        page: int = 1,
        page_size: int = 10,
        title: Optional[str] = None,
        release_year: Optional[int] = None,
        genre_name: Optional[str] = None,
    ) -> tuple[list[Movie], int]:
        query = self.db.query(Movie).options(joinedload(Movie.director), joinedload(Movie.genres))

        if title:
            query = query.filter(Movie.title.ilike(f"%{title}%"))
        if release_year:
            query = query.filter(Movie.release_year == release_year)
        if genre_name:
            query = query.join(Movie.genres).filter(Genre.name == genre_name)

        total_items = query.count()
        offset = (page - 1) * page_size
        movies = query.offset(offset).limit(page_size).all()

        return movies, total_items

    def get_movie_with_stats(self, movie_id: int) -> Optional[tuple[Movie, Optional[float], int]]:
        movie = (
            self.db.query(Movie)
            .options(joinedload(Movie.director), joinedload(Movie.genres))
            .filter(Movie.id == movie_id)
            .first()
        )
        if not movie:
            return None

        rating_stats = (
            self.db.query(func.avg(MovieRating.score).label("avg_rating"), func.count(MovieRating.id).label("count"))
            .filter(MovieRating.movie_id == movie_id)
            .first()
        )

        avg_rating = float(rating_stats.avg_rating) if rating_stats.avg_rating else None
        ratings_count = rating_stats.count or 0

        return movie, avg_rating, ratings_count

    def get_list_with_stats(
        self,
        page: int = 1,
        page_size: int = 10,
        title: Optional[str] = None,
        release_year: Optional[int] = None,
        genre_name: Optional[str] = None,
    ) -> tuple[list[tuple[Movie, Optional[float], int]], int]:
        query = self.db.query(Movie).options(joinedload(Movie.director), joinedload(Movie.genres))

        if title:
            query = query.filter(Movie.title.ilike(f"%{title}%"))
        if release_year:
            query = query.filter(Movie.release_year == release_year)
        if genre_name:
            query = query.join(Movie.genres).filter(Genre.name == genre_name)

        total_items = query.count()
        offset = (page - 1) * page_size
        movies = query.offset(offset).limit(page_size).all()

        movie_ids = [movie.id for movie in movies]
        rating_stats = (
            self.db.query(
                MovieRating.movie_id,
                func.avg(MovieRating.score).label("avg_rating"),
                func.count(MovieRating.id).label("count"),
            )
            .filter(MovieRating.movie_id.in_(movie_ids))
            .group_by(MovieRating.movie_id)
            .all()
        )

        stats_dict = {stat.movie_id: (float(stat.avg_rating) if stat.avg_rating else None, stat.count or 0) for stat in rating_stats}

        movies_with_stats = [(movie, stats_dict.get(movie.id, (None, 0))[0], stats_dict.get(movie.id, (None, 0))[1]) for movie in movies]

        return movies_with_stats, total_items
