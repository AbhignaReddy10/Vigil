"""
Centralized application settings.

Why this exists: hardcoding config values (database URLs, secret keys)
scattered across files is how real projects end up with secrets committed
to git by accident. Every setting is read from environment variables in
ONE place, with safe defaults for local development only.

Pydantic validates these at startup — if a required setting is missing
or malformed, the app fails immediately with a clear error instead of
crashing confusingly later, mid-request.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # App
    environment: str = "development"
    project_name: str = "Vigil"
    api_v1_prefix: str = "/api/v1"

    # Security
    # NOTE: this default is ONLY for local dev so the app boots without
    # a .env file present. Production MUST override this via a real
    # environment variable — never commit a real secret key to git.
    secret_key: str = "dev-only-insecure-secret-change-me"
    access_token_expire_minutes: int = 60 * 24  # 24 hours

    # Database
    database_url: str = "sqlite:///./vigil_dev.db"

    # CORS — which frontend origins may call this API
    cors_origins: list[str] = ["http://localhost:5173", "http://localhost:3000"]


settings = Settings()
