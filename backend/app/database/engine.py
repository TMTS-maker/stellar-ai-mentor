"""
Stellecta LucidAI Backend - Database Engine

SQLAlchemy 2.0 engine and session management.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

# ============================================================================
# SQLALCHEMY ENGINE
# ============================================================================

engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,  # Verify connections before using
    pool_size=10,  # Number of connections to maintain
    max_overflow=20,  # Additional connections allowed
    echo=settings.app_debug,  # Log SQL in development
)

# ============================================================================
# SESSION FACTORY
# ============================================================================

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# ============================================================================
# BASE MODEL
# ============================================================================

Base = declarative_base()


# ============================================================================
# DEPENDENCY INJECTION
# ============================================================================

def get_db():
    """
    FastAPI dependency for database sessions.

    Usage:
        @app.get("/items")
        def get_items(db: Session = Depends(get_db)):
            return db.query(Item).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
