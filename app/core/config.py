import os

from dotenv import load_dotenv

load_dotenv()


class Settings:

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


settings = Settings()
