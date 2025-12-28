from typing import Any, Optional
from pydantic import BaseModel


class SuccessResponse(BaseModel):
    status: str = "success"
    data: Any


class ErrorDetail(BaseModel):
    code: int
    message: str


class ErrorResponse(BaseModel):
    status: str = "failure"
    error: ErrorDetail

