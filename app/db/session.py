# app/db/session.py

"""
Database engine and session management module.

Module Purpose:
    Configures the SQLAlchemy database engine and session factory used
    throughout the application. Provides a dependency function for
    obtaining and properly disposing database sessions.

Extended Description:
    This module is responsible for initializing the SQLAlchemy engine
    using application configuration settings and creating a reusable
    session factory. It also exposes a generator-based dependency that
    provides database sessions and guarantees proper resource cleanup.

    During initialization, the module validates the database connection
    configuration and converts common SQLAlchemy configuration errors
    into application-level runtime exceptions with clearer messages.

Main Responsibilities:
    - Create and configure the SQLAlchemy engine.
    - Create a reusable session factory.
    - Validate database configuration during startup.
    - Provide database sessions to application components.
    - Ensure proper session cleanup.

Key Components:
    - engine: SQLAlchemy database engine.
    - SessionLocal: Session factory used to create database sessions.
    - get_db(): Session provider and cleanup dependency.

Dependencies:
    - sqlalchemy.create_engine
    - sqlalchemy.orm.sessionmaker
    - sqlalchemy.exc.ArgumentError
    - sqlalchemy.exc.NoSuchModuleError
    - app.core.config.settings

Side Effects:
    - Creates a database engine during module import.
    - Validates database connection configuration.
    - Raises runtime exceptions if configuration is invalid.

Input/Output Behavior:
    Input:
        Database configuration from application settings.

    Output:
        Configured engine, session factory, and session provider.

Error Handling Strategy:
    - Converts invalid SQLAlchemy configuration errors into RuntimeError.
    - Converts missing database driver errors into RuntimeError.
    - Ensures session cleanup through a finally block.

Performance Considerations:
    - Engine creation occurs once during module import.
    - Session objects are created on demand.
    - Session lifecycle management minimizes resource leakage.

Thread Safety / Concurrency Notes:
    - SQLAlchemy engines are designed for concurrent use.
    - Individual session instances are not thread-safe.
    - Each request or operation should use its own session instance.

Usage Example:
    >>> from app.db.session import get_db
    >>>
    >>> for db in get_db():
    ...     result = db.execute(...)

Limitations:
    - Assumes a valid DATABASE_URL is available.
    - Does not implement connection retry strategies.
    - Does not manage transactions automatically.

Version / Maintenance Notes:
    Database initialization behavior should remain centralized to avoid
    inconsistent engine or session configurations throughout the
    application.
"""

from sqlalchemy import create_engine
from sqlalchemy.exc import (
    ArgumentError,
    NoSuchModuleError,
)
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

try:
    engine = create_engine(
        settings.DATABASE_URL,
        echo=False,
    )

    SessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    )

except ArgumentError as exc:
    raise RuntimeError(
        "Invalid database URL or SQLAlchemy configuration."
    ) from exc

except NoSuchModuleError as exc:
    raise RuntimeError(
        "Database driver not found or not installed."
    ) from exc


def get_db():
    """
    Provide a database session and guarantee proper cleanup.

    Extended Description:
        Creates a new SQLAlchemy session using the configured session
        factory and yields it to the caller. The session is automatically
        closed after usage, regardless of whether the operation succeeds
        or fails.

        This function is commonly used as a dependency provider in web
        frameworks and service layers that require database access.

    Yields:
        sqlalchemy.orm.Session:
            An active SQLAlchemy database session.

    Raises:
        RuntimeError:
            May indirectly propagate runtime errors related to database
            initialization if the session factory was not successfully
            configured.

    Notes:
        - The yielded session should not be shared across threads.
        - Session lifecycle management is handled automatically.
        - Transaction management is the responsibility of the caller.

    Side Effects:
        - Creates a new database session.
        - Closes the session after execution.

    Examples:
        >>> for db in get_db():
        ...     users = db.query(User).all()

        >>> # Dependency injection example
        >>> def service(db=Depends(get_db)):
        ...     pass
    """

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()
