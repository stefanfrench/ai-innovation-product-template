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

    # LiteLLM - supports OpenAI, Azure, Anthropic, local models, and 100+ others
    # See: https://docs.litellm.ai/docs/providers
    litellm_model: str = "gpt-4o-mini"  # Default model
    openai_api_key: str | None = None
    azure_api_key: str | None = None
    azure_api_base: str | None = None
    azure_api_version: str = "2024-02-15-preview"
    anthropic_api_key: str | None = None

    # For local models (Ollama)
    ollama_base_url: str = "http://localhost:11434"

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
