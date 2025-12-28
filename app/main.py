from fastapi import FastAPI
from app.config import settings

app = FastAPI(title=settings.APP_NAME, version="0.1.0", debug=settings.DEBUG)


@app.get("/")
def root():
    return {"message": "Movie Rating System API"}

