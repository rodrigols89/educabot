"""
Configuration module for application settings.

This module loads environment variables and provides
centralized configuration for the system.
"""

import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    """
    Application settings loader.

    Attributes
    ----------
    DATABASE_URL : str
        Database connection string.

    EVOLUTION_API_URL : str
        Evolution API base URL.

    EVOLUTION_INSTANCE : str
        Evolution instance name.

    EVOLUTION_API_KEY : str
        Evolution API authentication key.
    """

    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "",
    )

    EVOLUTION_API_URL: str = os.getenv(
        "EVOLUTION_API_URL",
        "",
    )

    EVOLUTION_INSTANCE: str = os.getenv(
        "EVOLUTION_INSTANCE",
        "",
    )

    EVOLUTION_API_KEY: str = os.getenv(
        "EVOLUTION_API_KEY",
        "",
    )


settings = Settings()
