from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
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


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Convert Pydantic validation errors to our error format."""
    errors = exc.errors()
    if errors:
        first_error = errors[0]
        loc = first_error.get("loc", [])
        field_path = " -> ".join(str(loc_item) for loc_item in loc if loc_item != "body")
        if not field_path:
            field_path = "body"
        message = first_error.get("msg", "Validation error")
        error_message = f"{field_path}: {message}"
    else:
        error_message = "Validation error"
    return error_response(message=error_message, status_code=422)


@app.get("/")
def root():
    return {"message": "Movie Rating System API"}
