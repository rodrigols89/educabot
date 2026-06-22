# app/db/base.py

"""
Database base model configuration module.

Module Purpose:
    Provides the application's declarative base class used by SQLAlchemy's
    ORM system. All ORM models should inherit from this shared base class
    to ensure consistent metadata registration and schema management.

Extended Description:
    This module centralizes the creation of the SQLAlchemy declarative base,
    which serves as the foundation for all mapped database entities within
    the application. By defining a single shared base object, SQLAlchemy
    can collect metadata from all model definitions and manage schema
    generation, migrations, and ORM mappings consistently.

Main Responsibilities:
    - Create a shared SQLAlchemy declarative base.
    - Provide a common inheritance root for ORM models.
    - Enable centralized metadata collection.

Key Components:
    - Base: SQLAlchemy declarative base instance.

Dependencies:
    - sqlalchemy.orm.declarative_base

Side Effects:
    - Creates a declarative base instance during module import.

Input/Output Behavior:
    Input:
        None.

    Output:
        Exposes a declarative base object for ORM model inheritance.

Error Handling Strategy:
    No explicit error handling is implemented. Any import-related errors
    are propagated by the Python runtime or SQLAlchemy.

Performance Considerations:
    The declarative base is created once at import time and introduces
    negligible runtime overhead.

Thread Safety / Concurrency Notes:
    The declarative base object is effectively immutable after creation
    and can be safely shared across threads. Thread safety of database
    operations depends on SQLAlchemy session management rather than this
    module.

Usage Example:
    >>> from app.db.base import Base
    >>>
    >>> class User(Base):
    ...     __tablename__ = "users"

Limitations:
    This module only defines the ORM base class and does not provide
    database connections, sessions, migrations, or model definitions.

Version / Maintenance Notes:
    Changes to the declarative base configuration may affect all ORM
    models inheriting from it and should be evaluated carefully.
"""

from sqlalchemy.orm import declarative_base

Base = declarative_base()
