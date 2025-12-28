from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.db.base import Base

genres_movie = Table(
    "genres_movie",
    Base.metadata,
    Column("movie_id", Integer, ForeignKey("movies.id"), primary_key=True),
    Column("genre_id", Integer, ForeignKey("genres.id"), primary_key=True),
)


class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    director_id = Column(Integer, ForeignKey("directors.id"), nullable=False)
    release_year = Column(Integer, nullable=False)
    cast = Column(String, nullable=True)

    director = relationship("Director", back_populates="movies")
    genres = relationship("Genre", secondary=genres_movie, back_populates="movies")
    ratings = relationship("MovieRating", back_populates="movie", cascade="all, delete-orphan")
