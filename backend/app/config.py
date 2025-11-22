"""
Application configuration using Pydantic settings.
Loads from environment variables with validation.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    """Application settings with environment variable support."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )

    # LLM Provider Settings
    openai_api_key: str = ""
    anthropic_api_key: str = ""
    google_api_key: str = ""
    lucidai_api_key: str = ""

    default_llm_provider: str = "openai"
    default_model: str = "gpt-4-turbo-preview"

    # Database
    database_url: str = "sqlite+aiosqlite:///./stellar.db"
    database_echo: bool = False

    # Application
    app_env: str = "development"
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    app_reload: bool = True
    cors_origins: str = "http://localhost:5173,http://localhost:3000"

    # Security
    secret_key: str = "change-me-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # Logging
    log_level: str = "INFO"

    # Feature Flags
    enable_gamification: bool = True
    enable_lvo: bool = True
    enable_hpem: bool = True
    enable_training_logger: bool = False

    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins into a list."""
        return [origin.strip() for origin in self.cors_origins.split(",")]


# Global settings instance
settings = Settings()
