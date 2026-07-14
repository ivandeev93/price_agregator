from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "Price Tracker"

    DATABASE_URL: str = (
        "postgresql+asyncpg://user:password@localhost:5432/app"
    )

    REDIS_URL: str = "redis://localhost:6379/0"

    CACHE_EXPIRE_SECONDS: int = 300

    CELERY_BROKER_URL: str = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/2"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()