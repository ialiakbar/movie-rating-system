from app.exceptions.base import BaseAPIException


class InvalidRatingScoreError(BaseAPIException):
    def __init__(self, score: int):
        super().__init__(status_code=422, message=f"Invalid score: {score}. Score must be between 1 and 10")


