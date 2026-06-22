# app/core/config.py

"""
Module Purpose:
    Provide centralized application configuration management by loading
    environment variables and exposing them through a shared settings object.

Extended Description:
    This module is responsible for reading configuration values from the
    operating system environment and optional .env files. It initializes
    environment loading during module import and maps configuration values
    to a dedicated settings container.

    The resulting settings instance acts as a single source of truth for
    application configuration, allowing other modules to access database,
    cache, authentication, and external service settings in a consistent
    manner.

Main Responsibilities:
    - Load environment variables from a .env file.
    - Define application configuration attributes.
    - Provide default values for selected settings.
    - Expose a globally accessible settings instance.
    - Centralize configuration retrieval logic.

Key Components:
    Settings:
        Configuration container that stores application settings loaded
        from environment variables.

    settings:
        Singleton-style instance of the Settings class used throughout
        the application.

Dependencies:
    - os:
        Used to retrieve environment variable values.
    - dotenv.load_dotenv:
        Loads variables from a .env file into the process environment.

Side Effects:
    - Loads environment variables from a .env file during module import.
    - Initializes configuration values immediately when the module is loaded.
    - Creates a global settings instance.

Input/Output Behavior:
    Inputs:
        - Environment variables available in the runtime environment.
        - Values defined in a .env file.

    Outputs:
        - A populated Settings object containing configuration values
          represented as strings.

Error Handling Strategy:
    - Missing environment variables do not raise exceptions.
    - Empty strings are used as fallback values for most configuration
      entries.
    - A predefined default URL is provided for the external API endpoint
      when no environment variable is supplied.

Performance Considerations:
    - Configuration values are resolved once during module import.
    - Environment lookups have negligible runtime overhead.
    - Subsequent access to configuration values is performed through
      in-memory attributes.

Thread Safety / Concurrency Notes:
    - The module exposes immutable configuration values after initialization.
    - Safe for concurrent read access in multithreaded environments.
    - No synchronization mechanisms are required because configuration
      values are not modified dynamically.

Usage Example:
    from app.core.config import settings

    database_uri = settings.DATABASE_CONNECTION_URI
    redis_uri = settings.CACHE_REDIS_URI

Limitations:
    - All configuration values are stored as strings without validation.
    - No type conversion or schema enforcement is performed.
    - Configuration changes made after module import are not automatically
      reflected in the existing settings instance.
    - Missing required values are not detected automatically.

Version / Maintenance Notes:
    - New configuration parameters should be added to the Settings class
      to preserve centralized configuration management.
    - Consider introducing validation and typed settings if application
      complexity increases.
    - The module should remain lightweight to avoid import-time overhead.
"""

import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    """
    Centralizes application settings loaded from environment variables.

    This class provides a single access point for configuration values
    related to database connections, authentication, Redis cache, and
    external service integrations. All settings are loaded during class
    initialization and exposed as class attributes.

    Attributes:
        DATABASE_URL (str):
            Primary database connection URL.

        CONFIG_SESSION_PHONE_VERSION (str):
            Configuration version used for phone session management.

        AUTHENTICATION_API_KEY (str):
            API key used to authenticate requests to protected services.

        DATABASE_PROVIDER (str):
            Name of the database provider used by the application.

        DATABASE_CONNECTION_URI (str):
            Complete database connection URI.

        CACHE_REDIS_URI (str):
            Redis server connection URI.

        CACHE_REDIS_PREFIX_KEY (str):
            Prefix applied to Redis keys for namespacing and isolation.

        EVOLUTION_API_URL (str):
            Base URL of the Evolution API.
            Defaults to "http://localhost:8080".

        EVOLUTION_INSTANCE (str):
            Identifier or name of the configured Evolution API instance.
    """

    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "",
    )

    CONFIG_SESSION_PHONE_VERSION: str = os.getenv(
        "CONFIG_SESSION_PHONE_VERSION",
        "",
    )

    AUTHENTICATION_API_KEY: str = os.getenv(
        "AUTHENTICATION_API_KEY",
        "",
    )

    DATABASE_PROVIDER: str = os.getenv(
        "DATABASE_PROVIDER",
        "",
    )

    DATABASE_CONNECTION_URI: str = os.getenv(
        "DATABASE_CONNECTION_URI",
        "",
    )

    CACHE_REDIS_URI: str = os.getenv(
        "CACHE_REDIS_URI",
        "",
    )

    CACHE_REDIS_PREFIX_KEY: str = os.getenv(
        "CACHE_REDIS_PREFIX_KEY",
        "",
    )

    EVOLUTION_API_URL: str = os.getenv(
        "EVOLUTION_API_URL",
        "http://localhost:8080",
    )

    EVOLUTION_INSTANCE: str = os.getenv(
        "EVOLUTION_INSTANCE",
        "",
    )


settings = Settings()
