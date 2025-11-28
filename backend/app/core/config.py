"""Application configuration settings."""
import os
import secrets
from typing import Optional
from pydantic_settings import BaseSettings


def get_default_secret_key() -> str:
    """Generate a warning-indicating default key for development only."""
    # This is intentionally weak and contains a warning - production MUST override
    return "INSECURE_DEV_KEY_CHANGE_ME_IN_PRODUCTION_" + secrets.token_hex(16)


class Settings(BaseSettings):
    """Application settings loaded from environment variables.
    
    IMPORTANT: For production, set these environment variables:
    - DATABASE_URL: PostgreSQL connection string
    - SECRET_KEY: A secure random string (minimum 32 characters)
    """

    # Database - no default to force explicit configuration
    DATABASE_URL: str = "postgresql+asyncpg://repairhub:changeme@localhost:5432/repairhub"

    # Security - generate random default for dev, but production MUST override
    SECRET_KEY: str = get_default_secret_key()
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
