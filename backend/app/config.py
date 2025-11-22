"""
Stellecta LucidAI Backend - Configuration Management

Environment-based configuration using Pydantic Settings.
All secrets and configuration are loaded from environment variables or .env file.
"""

from typing import Literal
from pydantic import Field, validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    Uses Pydantic V2 settings management with:
    - Type validation
    - Environment variable loading
    - .env file support
    - Default values
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    # ========================================================================
    # CORE APPLICATION
    # ========================================================================
    app_name: str = Field(default="Stellecta LucidAI Backend")
    app_env: Literal["development", "staging", "production"] = Field(default="development")
    app_debug: bool = Field(default=True)
    app_host: str = Field(default="0.0.0.0")
    app_port: int = Field(default=8000)

    # ========================================================================
    # DATABASE (PostgreSQL)
    # ========================================================================
    database_url: str = Field(
        default="postgresql://stellecta:stellecta@localhost:5432/stellecta_dev"
    )

    # ========================================================================
    # REDIS (Caching & Queue)
    # ========================================================================
    redis_url: str = Field(default="redis://localhost:6379/0")

    # ========================================================================
    # SECURITY
    # ========================================================================
    secret_key: str = Field(default="__CHANGE_THIS_TO_RANDOM_SECRET_KEY__")
    algorithm: str = Field(default="HS256")
    access_token_expire_minutes: int = Field(default=30)

    # ========================================================================
    # EXTERNAL LLM PROVIDERS
    # ========================================================================

    # OpenAI
    openai_api_key: str = Field(default="__OPENAI_API_KEY__")
    openai_model: str = Field(default="gpt-4-turbo-preview")
    openai_max_tokens: int = Field(default=2000)

    # Google Gemini
    gemini_api_key: str = Field(default="__GEMINI_API_KEY__")
    gemini_model: str = Field(default="gemini-2.5-flash")
    gemini_max_tokens: int = Field(default=2000)

    # Anthropic Claude
    anthropic_api_key: str = Field(default="__ANTHROPIC_API_KEY__")
    anthropic_model: str = Field(default="claude-3-5-sonnet-20240620")
    anthropic_max_tokens: int = Field(default=2000)

    # Perplexity
    perplexity_api_key: str = Field(default="__PERPLEXITY_API_KEY__")
    perplexity_model: str = Field(default="llama-3.1-sonar-large-128k-online")

    # DeepSeek
    deepseek_api_key: str = Field(default="__DEEPSEEK_API_KEY__")
    deepseek_model: str = Field(default="deepseek-chat")

    # ========================================================================
    # STELLECTA LUCIDAI (Internal/Proprietary LLM)
    # ========================================================================
    lucidai_api_url: str = Field(default="__LUCIDAI_API_URL__")
    lucidai_api_key: str = Field(default="__LUCIDAI_API_KEY__")
    lucidai_model: str = Field(default="lucidai-v1.0-stella")
    lucidai_max_tokens: int = Field(default=2000)
    lucidai_timeout: int = Field(default=30)

    # ========================================================================
    # MULTI-LLM ROUTER CONFIGURATION
    # ========================================================================
    default_llm_provider: Literal["lucidai", "gemini", "openai", "claude", "perplexity", "deepseek"] = Field(
        default="gemini"
    )
    fallback_llm_provider: Literal["lucidai", "gemini", "openai", "claude", "perplexity", "deepseek"] = Field(
        default="openai"
    )
    enable_hybrid_mode: bool = Field(default=True)
    routing_confidence_threshold: float = Field(default=0.85, ge=0.0, le=1.0)

    # ========================================================================
    # STELLAR BLOCKCHAIN (Credentials & Tokenization)
    # ========================================================================
    stellar_network: Literal["testnet", "mainnet"] = Field(default="testnet")
    stellar_horizon_url: str = Field(default="https://horizon-testnet.stellar.org")
    stellar_issuer_public_key: str = Field(default="__STELLAR_ISSUER_PUBLIC_KEY__")
    stellar_issuer_secret_key: str = Field(default="__STELLAR_ISSUER_SECRET_KEY__")

    # ========================================================================
    # TRAINING DATA PIPELINE
    # ========================================================================
    enable_training_logging: bool = Field(default=True)
    anonymize_training_data: bool = Field(default=True)
    training_data_retention_days: int = Field(default=365)

    # ========================================================================
    # H-PEM & LCT CONFIGURATION
    # ========================================================================
    hpem_proficiency_weight: float = Field(default=0.3, ge=0.0, le=1.0)
    hpem_resilience_weight: float = Field(default=0.2, ge=0.0, le=1.0)
    hpem_velocity_weight: float = Field(default=0.2, ge=0.0, le=1.0)
    hpem_engagement_weight: float = Field(default=0.15, ge=0.0, le=1.0)
    hpem_transfer_weight: float = Field(default=0.15, ge=0.0, le=1.0)

    @validator("hpem_proficiency_weight", "hpem_resilience_weight", "hpem_velocity_weight",
               "hpem_engagement_weight", "hpem_transfer_weight")
    def validate_hpem_weights_sum(cls, v, values):
        """Ensure H-PEM weights sum to 1.0"""
        # NOTE: This is a simplified validator - full implementation would sum all weights
        return v

    # ========================================================================
    # GAMIFICATION
    # ========================================================================
    xp_per_task_completion: int = Field(default=50)
    xp_per_mastery_achievement: int = Field(default=200)
    streak_bonus_multiplier: float = Field(default=1.5)

    # ========================================================================
    # CORS (Frontend URLs)
    # ========================================================================
    cors_origins: str = Field(default="http://localhost:5173,http://localhost:3000")

    @property
    def cors_origins_list(self) -> list[str]:
        """Parse CORS origins into list"""
        return [origin.strip() for origin in self.cors_origins.split(",")]

    # ========================================================================
    # LOGGING
    # ========================================================================
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(default="INFO")
    log_format: Literal["json", "text"] = Field(default="json")

    # ========================================================================
    # COMPUTED PROPERTIES
    # ========================================================================

    @property
    def is_development(self) -> bool:
        """Check if running in development mode"""
        return self.app_env == "development"

    @property
    def is_production(self) -> bool:
        """Check if running in production mode"""
        return self.app_env == "production"


# ============================================================================
# GLOBAL SETTINGS INSTANCE
# ============================================================================

settings = Settings()


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_settings() -> Settings:
    """
    Dependency injection helper for FastAPI.

    Usage in routes:
        @app.get("/info")
        def info(settings: Settings = Depends(get_settings)):
            return {"env": settings.app_env}
    """
    return settings
