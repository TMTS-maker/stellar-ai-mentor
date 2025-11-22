"""
Configuration Settings for Stellecta Platform

Uses Pydantic Settings for environment variable management
"""
from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # Application
    APP_NAME: str = "Stellecta API"
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"
    DEBUG: bool = True

    # Database
    DATABASE_URL: str = "postgresql://stellecta:dev_password@postgres:5432/stellecta"

    # Redis
    REDIS_URL: str = "redis://redis:6379/0"

    # JWT Authentication
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # LLM API Keys
    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""
    LUCIDAI_ENDPOINT: str = ""
    LUCIDAI_API_KEY: str = ""

    # Stellar Blockchain
    STELLAR_NETWORK: str = "testnet"  # "testnet" or "mainnet"
    STELLAR_HORIZON_URL: str = "https://horizon-testnet.stellar.org"
    STELLAR_ISSUER_SECRET: str = ""
    STELLAR_ISSUER_PUBLIC: str = ""

    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173"
    ]

    # Gamification
    XP_PER_MESSAGE: int = 10
    XP_PER_CORRECT_ANSWER: int = 50
    STREAK_BONUS_XP: int = 20

    # LLM Router Configuration
    DEFAULT_LLM_PROVIDER: str = "lucidai"  # "lucidai", "openai", or "anthropic"
    MAX_TOKENS: int = 1000
    TEMPERATURE: float = 0.7

    # Celery (for background tasks)
    CELERY_BROKER_URL: str = "redis://redis:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://redis:6379/2"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

# Create global settings instance
settings = Settings()
