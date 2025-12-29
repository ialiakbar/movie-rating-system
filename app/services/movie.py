from typing import Optional
from sqlalchemy.orm import Session
from app.repositories.movie import MovieRepository
from app.repositories.director import DirectorRepository
from app.repositories.genre import GenreRepository
from app.schemas.movie import MovieCreate, MovieUpdate, MovieListItem, MovieDetail, MovieListResponse
from app.schemas.director import DirectorBase, DirectorDetail
from app.exceptions.movie import MovieNotFoundError, DirectorNotFoundError, GenreNotFoundError, InvalidReleaseYearError
from app.models.movie import Movie


class MovieService:
    def __init__(self, db: Session, director_repo: DirectorRepository, genre_repo: GenreRepository, movie_repo: MovieRepository):
        self.db = db
        self.movie_repo = movie_repo
        self.director_repo = director_repo
        self.genre_repo = genre_repo

    def get_movie_list(
        self, page: int = 1, page_size: int = 10, title: Optional[str] = None, release_year: Optional[int] = None, genre: Optional[str] = None
    ) -> MovieListResponse:
        if release_year is not None and (not isinstance(release_year, int) or release_year < 1800 or release_year > 2100):
            raise InvalidReleaseYearError(release_year)

        movies_with_stats, total_items = self.movie_repo.get_list_with_stats(page=page, page_size=page_size, title=title, release_year=release_year, genre_name=genre)

        items = []
        for movie, avg_rating, ratings_count in movies_with_stats:
            items.append(
                MovieListItem(
                    id=movie.id,
                    title=movie.title,
                    release_year=movie.release_year,
                    director=DirectorBase(id=movie.director.id, name=movie.director.name),
                    genres=[genre.name for genre in movie.genres],
                    average_rating=round(avg_rating, 2) if avg_rating else None,
                    ratings_count=ratings_count,
                )
            )

        return MovieListResponse(page=page, page_size=page_size, total_items=total_items, items=items)

    def get_movie_by_id(self, movie_id: int) -> MovieDetail:
        result = self.movie_repo.get_movie_with_stats(movie_id)
        if not result:
            raise MovieNotFoundError(movie_id)

        movie, avg_rating, ratings_count = result

        return MovieDetail(
            id=movie.id,
            title=movie.title,
            release_year=movie.release_year,
            cast=movie.cast,
            description=movie.description,
            director=DirectorDetail(id=movie.director.id, name=movie.director.name, birth_year=movie.director.birth_year, description=movie.director.description),
            genres=[genre.name for genre in movie.genres],
            average_rating=round(avg_rating, 2) if avg_rating else None,
            ratings_count=ratings_count,
        )

    def create_movie(self, movie_data: MovieCreate) -> MovieDetail:
        director = self.director_repo.get_by_id(movie_data.director_id)
        if not director:
            raise DirectorNotFoundError(movie_data.director_id)

        if movie_data.genres:
            genres = self.genre_repo.get_by_ids(movie_data.genres)
            if len(genres) != len(movie_data.genres):
                found_ids = {g.id for g in genres}
                missing_ids = [gid for gid in movie_data.genres if gid not in found_ids]
                raise GenreNotFoundError(missing_ids[0] if missing_ids else 0)

        movie = self.movie_repo.create(
            title=movie_data.title,
            director_id=movie_data.director_id,
            release_year=movie_data.release_year,
            cast=movie_data.cast,
            genre_ids=movie_data.genres,
        )

        return MovieDetail(
            id=movie.id,
            title=movie.title,
            release_year=movie.release_year,
            cast=movie.cast,
            description=movie.description,
            director=DirectorDetail(id=movie.director.id, name=movie.director.name, birth_year=movie.director.birth_year, description=movie.director.description),
            genres=[genre.name for genre in movie.genres],
            average_rating=None,
            ratings_count=0,
        )

    def update_movie(self, movie_id: int, movie_data: MovieUpdate) -> MovieDetail:
        movie = self.movie_repo.get_by_id(movie_id)
        if not movie:
            raise MovieNotFoundError(movie_id)

        update_data = {}
        if movie_data.title is not None:
            update_data["title"] = movie_data.title
        if movie_data.release_year is not None:
            update_data["release_year"] = movie_data.release_year
        if movie_data.cast is not None:
            update_data["cast"] = movie_data.cast

        if update_data:
            self.movie_repo.update(movie, **update_data)

        if movie_data.genres is not None:
            genres = self.genre_repo.get_by_ids(movie_data.genres)
            if len(genres) != len(movie_data.genres):
                found_ids = {g.id for g in genres}
                missing_ids = [gid for gid in movie_data.genres if gid not in found_ids]
                raise GenreNotFoundError(missing_ids[0] if missing_ids else 0)
            self.movie_repo.update_genres(movie, movie_data.genres)

        self.db.refresh(movie)
        result = self.movie_repo.get_movie_with_stats(movie_id)
        if not result:
            raise MovieNotFoundError(movie_id)

        movie, avg_rating, ratings_count = result

        return MovieDetail(
            id=movie.id,
            title=movie.title,
            release_year=movie.release_year,
            cast=movie.cast,
            description=movie.description,
            director=DirectorDetail(id=movie.director.id, name=movie.director.name, birth_year=movie.director.birth_year, description=movie.director.description),
            genres=[genre.name for genre in movie.genres],
            average_rating=round(avg_rating, 2) if avg_rating else None,
            ratings_count=ratings_count,
        )

    def delete_movie(self, movie_id: int) -> None:
        movie = self.movie_repo.get_by_id(movie_id)
        if not movie:
            raise MovieNotFoundError(movie_id)

        self.movie_repo.delete(movie)

