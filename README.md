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
3. Start PostgreSQL database: `docker-compose up -d`
4. Copy `.env.example` to `.env` and configure (already matches docker-compose defaults)
5. Run migrations: `alembic upgrade head`
6. Seed database: See scripts/ directory
7. Start server: `poetry run python run.py`

## Docker Compose

The project includes a `docker-compose.yml` file to run PostgreSQL locally:

```bash
# Start database
docker-compose up -d

# Stop database
docker-compose down

# View logs
docker-compose logs -f db
```

## API Base Path

All endpoints are under `/api/v1`

