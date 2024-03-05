"""For core settings from ENV."""

import functools
import pathlib

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Project settings."""

    BASE_DIR: pathlib.Path = pathlib.Path(__file__).resolve().parent.parent
    ENVIRONMENT: str = "local"

    DEBUG: bool = True

    DATABASE_URI: str = "postgresql://sber_tracker:sber_tracker@db:5432/sber_tracker"
    POSTGRES_HOST: str = "db"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "sber_tracker"
    POSTGRES_PASSWORD: str = "sber_tracker"
    POSTGRES_DB: str = "sber_tracker"

    model_config = SettingsConfigDict(env_file="./.env", env_file_encoding="utf-8")

    @property
    def postgres_dsn(self) -> str:
        database = self.POSTGRES_DB
        return (
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{database}"
        )

@functools.lru_cache
def settings() -> Settings:
    return Settings()
