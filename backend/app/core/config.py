"""
Application configuration using Pydantic Settings.
All config is loaded from environment variables.
"""

from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # App
    app_name: str = "CapStack API"
    app_env: Literal["development", "staging", "production"] = "development"
    debug: bool = True

    # Database
    # SQLite for local dev, PostgreSQL for production
    database_url: str = "sqlite+aiosqlite:///./capstack.db"

    # LLM - Azure OpenAI (recommended) or OpenAI
    llm_model: str = "gpt-4o-mini"
    azure_openai_api_key: str | None = None
    azure_openai_endpoint: str | None = None
    azure_openai_api_version: str = "2024-10-21"
    openai_api_key: str | None = None

    # Auth (optional - set API_KEY to enable simple key-based auth on /api/* routes)
    api_key: str | None = None

    # CORS
    cors_origins: list[str] = ["http://localhost:5173", "http://localhost:3000"]

    @property
    def is_production(self) -> bool:
        return self.app_env == "production"


@lru_cache
def get_settings() -> Settings:
    """Cached settings instance."""
    return Settings()
