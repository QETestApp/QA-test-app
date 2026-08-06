"""Application configuration settings loaded from environment variables."""

from pathlib import Path
from typing import Any

from pydantic import Field, ValidationError, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


def _parse_csv(value: str | None, default: list[str] | None = None) -> list[str]:
    """Parse comma-separated values from the environment into a list."""
    if value is None:
        return default or []

    cleaned = value.strip()
    if not cleaned or cleaned == "*":
        return ["*"]

    return [item.strip() for item in cleaned.split(",") if item.strip()]


class Settings(BaseSettings):
    """Central application settings used across the backend."""

    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parent.parent / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    APP_NAME: str = "QA Test Playground API"
    APP_ENV: str = "development"
    APP_VERSION: str = "1.0.0"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    API_PREFIX: str = "/api/v1"
    DATABASE_URL: str = "sqlite:///./qa_playground.db"
    JWT_SECRET: str = Field(..., min_length=1)
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    LOG_LEVEL: str = "INFO"
    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000"
    ALLOW_CREDENTIALS: bool = True
    ALLOWED_METHODS: str = "*"
    ALLOWED_HEADERS: str = "*"

    @field_validator("LOG_LEVEL", mode="before")
    @classmethod
    def normalize_log_level(cls, value: Any) -> str:
        if value is None:
            return "INFO"
        return str(value).upper()

    @field_validator("API_PREFIX", mode="before")
    @classmethod
    def normalize_api_prefix(cls, value: Any) -> str:
        if value is None:
            return "/api/v1"
        normalized = str(value).strip()
        if not normalized.startswith("/"):
            normalized = f"/{normalized}"
        return normalized.rstrip("/") or "/"

    @property
    def cors_origins(self) -> list[str]:
        return _parse_csv(self.CORS_ORIGINS)

    @property
    def allowed_methods(self) -> list[str]:
        return _parse_csv(self.ALLOWED_METHODS)

    @property
    def allowed_headers(self) -> list[str]:
        return _parse_csv(self.ALLOWED_HEADERS)

    @property
    def is_development(self) -> bool:
        return self.APP_ENV.lower() == "development"

    @property
    def is_production(self) -> bool:
        return self.APP_ENV.lower() == "production"


try:
    settings = Settings()
except ValidationError as exc:
    raise RuntimeError(
        f"Invalid application configuration. Please provide all required environment variables: {exc}"
    ) from exc
