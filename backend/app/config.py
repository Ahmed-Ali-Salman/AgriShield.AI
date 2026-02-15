"""
AgriShield AI — Application Configuration.

Centralizes all environment-driven settings using Pydantic BaseSettings.
Single Responsibility: this module's only job is configuration loading.
"""

from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Immutable application settings loaded from environment variables."""

    # --- Application ---
    APP_NAME: str = "AgriShield AI"
    APP_ENV: str = "development"
    APP_DEBUG: bool = True
    APP_PORT: int = 8000
    APP_SECRET_KEY: str = "change-this-in-production"

    # --- Database ---
    DATABASE_URL: str = "postgresql+asyncpg://agrishield:password@localhost:5432/agrishield_db"

    # --- JWT ---
    JWT_SECRET_KEY: str = "change-this-jwt-secret"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # --- CORS ---
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]

    # --- Email ---
    SMTP_HOST: str = ""
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""

    # --- Twilio ---
    TWILIO_ACCOUNT_SID: str = ""
    TWILIO_AUTH_TOKEN: str = ""
    TWILIO_PHONE_NUMBER: str = ""

    # --- External APIs ---
    CVE_API_BASE_URL: str = "https://services.nvd.nist.gov/rest/json/cves/2.0"

    # --- ML ---
    MLFLOW_TRACKING_URI: str = "http://localhost:5000"
    MODEL_ARTIFACTS_PATH: str = "./ml_artifacts"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    """Cached settings singleton."""
    return Settings()


settings = get_settings()
