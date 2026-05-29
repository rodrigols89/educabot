"""
Database session manager.

Provides SQLAlchemy engine and session factory.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

engine = create_engine(settings.DATABASE_URL, echo=True)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db():
    """
    Provide database session dependency.

    Yields
    ------
    Session
        SQLAlchemy session instance.

    Examples
    --------
    >>> db = next(get_db())
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
