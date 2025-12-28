from fastapi import FastAPI

app = FastAPI(title="Movie Rating System", version="0.1.0")


@app.get("/")
def root():
    return {"message": "Movie Rating System API"}

