# Movie Rating System

Backend API for managing movies, directors, genres, and ratings.

## Tech Stack

- Python 3.11+
- FastAPI
- SQLAlchemy ORM
- PostgreSQL
- Poetry (dependency management)
- Alembic (database migrations)

## Project Structure

```
project_root/
├── app/
│   ├── controller/      # FastAPI route handlers
│   ├── services/        # Business logic layer
│   ├── repositories/    # Data access layer
│   ├── models/          # SQLAlchemy models
│   ├── schemas/         # Pydantic schemas
│   ├── db/              # Database configuration
│   ├── exceptions/       # Custom exceptions
│   ├── utils/           # Utility functions
│   └── main.py          # FastAPI application
├── alembic/             # Database migrations
├── scripts/             # Utility scripts
├── pyproject.toml       # Poetry configuration
├── docker-compose.yml   # PostgreSQL setup
└── run.py               # Server entry point
```

## Setup

1. Install Poetry: `curl -sSL https://install.python-poetry.org | python3 -`
2. Install dependencies: `poetry install`
3. Start PostgreSQL database: `docker-compose up -d`
4. Copy `.env.example` to `.env` and configure (already matches docker-compose defaults)
5. Run migrations: `poetry run alembic upgrade head`
6. Start server: `poetry run python run.py`

The server will be available at `http://localhost:8000`

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

## API Documentation

All endpoints are under `/api/v1`

### Base URL
- Development: `http://localhost:8000/api/v1`

### Response Format

All responses use an envelope format:

**Success Response:**
```json
{
  "status": "success",
  "data": { ... }
}
```

**Error Response:**
```json
{
  "status": "failure",
  "error": {
    "code": 404,
    "message": "Movie not found"
  }
}
```

### Endpoints

#### Movies

##### GET /api/v1/movies
Get paginated list of movies with filtering.

**Query Parameters:**
- `page` (int, default=1, min=1): Page number
- `page_size` (int, default=10, min=1, max=100): Items per page
- `title` (string, optional): Filter by title (partial match, case-insensitive)
- `release_year` (int, optional): Filter by exact release year
- `genre` (string, optional): Filter by genre name

**Response:**
```json
{
  "status": "success",
  "data": {
    "page": 1,
    "page_size": 10,
    "total_items": 50,
    "items": [
      {
        "id": 1,
        "title": "The Matrix",
        "release_year": 1999,
        "director": {
          "id": 1,
          "name": "Lana Wachowski"
        },
        "genres": ["Action", "Sci-Fi"],
        "average_rating": 8.7,
        "ratings_count": 150
      }
    ]
  }
}
```

##### GET /api/v1/movies/{movie_id}
Get movie details by ID.

**Response:**
```json
{
  "status": "success",
  "data": {
    "id": 1,
    "title": "The Matrix",
    "release_year": 1999,
    "cast": "Keanu Reeves, Laurence Fishburne",
    "description": "A computer hacker learns about the true nature of reality",
    "director": {
      "id": 1,
      "name": "Lana Wachowski",
      "birth_year": 1965,
      "description": "American film director"
    },
    "genres": ["Action", "Sci-Fi"],
    "average_rating": 8.7,
    "ratings_count": 150
  }
}
```

**Errors:**
- `404`: Movie not found

##### POST /api/v1/movies
Create a new movie.

**Request Body:**
```json
{
  "title": "Inception",
  "director_id": 2,
  "release_year": 2010,
  "cast": "Leonardo DiCaprio, Marion Cotillard",
  "genres": [1, 3]
}
```

**Response:** `201 Created`
```json
{
  "status": "success",
  "data": {
    "id": 2,
    "title": "Inception",
    "release_year": 2010,
    "cast": "Leonardo DiCaprio, Marion Cotillard",
    "description": null,
    "director": { ... },
    "genres": ["Action", "Thriller"],
    "average_rating": null,
    "ratings_count": 0
  }
}
```

**Errors:**
- `422`: Invalid director_id or genre_id (not found)

##### PUT /api/v1/movies/{movie_id}
Update a movie (partial update allowed).

**Request Body (all fields optional):**
```json
{
  "title": "Inception 2",
  "release_year": 2011,
  "cast": "Updated cast",
  "genres": [1, 2, 3]
}
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "id": 2,
    "title": "Inception 2",
    ...
  }
}
```

**Errors:**
- `404`: Movie not found
- `422`: Invalid genre_id (not found)

##### DELETE /api/v1/movies/{movie_id}
Delete a movie.

**Response:** `204 No Content` (empty body)

**Errors:**
- `404`: Movie not found

#### Ratings

##### POST /api/v1/movies/{movie_id}/ratings
Create a rating for a movie.

**Request Body:**
```json
{
  "score": 8
}
```

**Response:** `201 Created`
```json
{
  "status": "success",
  "data": {
    "rating_id": 1,
    "movie_id": 1,
    "score": 8,
    "created_at": "2024-01-15T10:30:00Z"
  }
}
```

**Errors:**
- `404`: Movie not found
- `422`: Invalid score (must be between 1 and 10)

## Error Codes

- `400`: Bad Request
- `404`: Not Found
- `422`: Unprocessable Entity (validation errors, invalid references)

## Development

### Running the Server

```bash
poetry run python run.py
```

The server runs with auto-reload enabled.

### Database Migrations

```bash
# Create a new migration
poetry run alembic revision --autogenerate -m "Description"

# Apply migrations
poetry run alembic upgrade head

# Rollback one migration
poetry run alembic downgrade -1

# Check current migration
poetry run alembic current
```

### Code Quality

```bash
# Format code
poetry run black .

# Lint code
poetry run ruff check .
```

## Architecture

The project follows a layered architecture with dependency injection:

- **Controllers**: Handle HTTP requests/responses, use `Depends()` for services
- **Services**: Business logic, use `Depends()` for repositories
- **Repositories**: Data access, use `Depends()` for database session
- **Models**: SQLAlchemy ORM models
- **Schemas**: Pydantic models for validation

All layers use FastAPI's dependency injection to ensure a single database session per request.

## License

MIT
