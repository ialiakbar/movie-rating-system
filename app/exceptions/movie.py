from app.exceptions.base import BaseAPIException


class MovieNotFoundError(BaseAPIException):
    def __init__(self, movie_id: int):
        super().__init__(status_code=404, message=f"Movie not found")


class InvalidReleaseYearError(BaseAPIException):
    def __init__(self, release_year: int):
        super().__init__(status_code=422, message=f"Invalid release_year: {release_year}")


class DirectorNotFoundError(BaseAPIException):
    def __init__(self, director_id: int):
        super().__init__(status_code=422, message=f"Director with id {director_id} not found")


class GenreNotFoundError(BaseAPIException):
    def __init__(self, genre_id: int):
        super().__init__(status_code=422, message=f"Genre with id {genre_id} not found")
