from typing import Optional
from pydantic import BaseModel


class DirectorBase(BaseModel):
    id: int
    name: str


class DirectorDetail(BaseModel):
    id: int
    name: str
    birth_year: Optional[int] = None
    description: Optional[str] = None


class DirectorResponse(DirectorDetail):
    pass

