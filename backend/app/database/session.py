"""
Database session management.

Provides SQLAlchemy session and engine setup.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from ..config import settings

# Create engine
engine = create_engine(
    settings.database_url,
    echo=settings.database_echo,
    future=True
)

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=Session
)


def get_db() -> Session:
    """
    Dependency for getting a database session.

    Yields:
        SQLAlchemy session

    Usage in FastAPI:
        @app.get("/endpoint")
        def endpoint(db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
