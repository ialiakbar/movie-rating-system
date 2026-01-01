from pydantic import BaseModel, Field
from datetime import datetime


class RatingCreate(BaseModel):
    score: int


class RatingResponse(BaseModel):
    rating_id: int
    movie_id: int
    score: int
    created_at: datetime  # This will be mapped from rated_at field

