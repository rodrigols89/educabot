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
    """

    DATABASE_URL: str = os.getenv("DATABASE_URL", "")


# Settings class instance
settings = Settings()
