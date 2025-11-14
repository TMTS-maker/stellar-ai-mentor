# Stellar AI Backend

FastAPI backend for the Stellar AI learning platform.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env with your configuration

# Run migrations
alembic upgrade head

# Start server
uvicorn app.main:app --reload
```

## Development

### Creating Migrations

```bash
alembic revision --autogenerate -m "Add new model"
alembic upgrade head
```

### Running Tests

```bash
pytest
```

## Project Structure

- `app/models/` - SQLAlchemy ORM models
- `app/schemas/` - Pydantic validation schemas
- `app/routers/` - FastAPI route handlers
- `app/services/` - Business logic and external service integrations
- `app/auth.py` - JWT authentication
- `app/main.py` - Application entry point

## API Documentation

Start the server and visit:
- http://localhost:8000/docs (Swagger UI)
- http://localhost:8000/redoc (ReDoc)
