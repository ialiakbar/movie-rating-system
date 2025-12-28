from typing import Optional
from sqlalchemy.orm import Session
from app.models.director import Director


class DirectorRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, director_id: int) -> Optional[Director]:
        return self.db.query(Director).filter(Director.id == director_id).first()

    def get_all(self) -> list[Director]:
        return self.db.query(Director).all()
