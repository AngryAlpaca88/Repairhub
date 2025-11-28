"""Application configuration settings."""
import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://repairhub:changeme@localhost:5432/repairhub"

    # Security
    SECRET_KEY: str = "changeme_super_secret_key_at_least_32_chars"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Business rules
    MINIMUM_PURE_PROFIT: float = 100.00

    # Application
    DEBUG: bool = False
    ENVIRONMENT: str = "development"

    class Config:
        """Pydantic config."""

        env_file = ".env"
        case_sensitive = True


settings = Settings()
