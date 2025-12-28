# Movie Rating System

Backend API for managing movies, directors, genres, and ratings.

## Tech Stack

- Python 3.11+
- FastAPI
- SQLAlchemy ORM
- PostgreSQL
- Poetry (dependency management)
- Alembic (database migrations)

## Setup

1. Install Poetry: `curl -sSL https://install.python-poetry.org | python3 -`
2. Install dependencies: `poetry install`
3. Copy `.env.example` to `.env` and configure
4. Run migrations: `alembic upgrade head`
5. Seed database: See scripts/ directory
6. Start server: `poetry run uvicorn app.main:app --reload`

## API Base Path

All endpoints are under `/api/v1`

