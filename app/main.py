from fastapi import FastAPI, Request
from app.config import settings
from app.controller.movie import router as movie_router
from app.controller.rating import router as rating_router
from app.exceptions.base import BaseAPIException
from app.utils.response import error_response

app = FastAPI(title=settings.APP_NAME, version="0.1.0", debug=settings.DEBUG)

app.include_router(movie_router, prefix="/api/v1/movies", tags=["movies"])
app.include_router(rating_router, prefix="/api/v1/movies/{movie_id}/ratings", tags=["ratings"])


@app.exception_handler(BaseAPIException)
async def api_exception_handler(request: Request, exc: BaseAPIException):
    return error_response(message=exc.message, status_code=exc.status_code)


@app.get("/")
def root():
    return {"message": "Movie Rating System API"}

