from functools import lru_cache
from typing import Literal

from pydantic import PositiveInt
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "GitHub Engineering Analytics"
    app_version: str = "0.1.0"

    mongodb_uri: str = "mongodb://localhost:27017"
    mongodb_database: str = "github_analytics"
    mongodb_server_selection_timeout_ms: PositiveInt = 2000

    github_token: str | None = None
    api_key: str | None = None

    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
