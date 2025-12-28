from typing import Optional
from sqlalchemy.orm import Session
from app.models.genre import Genre


class GenreRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, genre_id: int) -> Optional[Genre]:
        return self.db.query(Genre).filter(Genre.id == genre_id).first()

    def get_by_ids(self, genre_ids: list[int]) -> list[Genre]:
        return self.db.query(Genre).filter(Genre.id.in_(genre_ids)).all()

    def get_by_name(self, name: str) -> Optional[Genre]:
        return self.db.query(Genre).filter(Genre.name == name).first()

    def get_all(self) -> list[Genre]:
        return self.db.query(Genre).all()
