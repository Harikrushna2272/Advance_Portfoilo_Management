# Configuration settings for StockAI
import os
from typing import List, Optional

try:
    from pydantic_settings import BaseSettings
    from pydantic import Field
except ImportError:
    from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Application settings with environment variable support."""

    # Application settings
    app_name: str = Field(default="StockAI", env="APP_NAME")
    app_version: str = Field(default="1.0.0", env="APP_VERSION")
    debug: bool = Field(default=False, env="DEBUG")

    # API Configuration
    api_key: Optional[str] = Field(default=None, env="ALPACA_API_KEY")
    api_secret: Optional[str] = Field(default=None, env="ALPACA_API_SECRET")
    base_url: str = Field(
        default="https://paper-api.alpaca.markets", env="ALPACA_BASE_URL"
    )

    # Stock Configuration
    stock_list: List[str] = Field(default=["AAPL", "TSLA", "GOOGL"], env="STOCK_LIST")

    # Model Configuration
    ensemble_model_paths: List[str] = Field(
        default=[
            "models/trained_rl_model_sac.pkl",
            "models/trained_rl_model_ppo.pkl",
            "models/trained_rl_model_a2c.pkl",
            "models/trained_rl_model_dqn.pkl",
            "models/trained_rl_model_td3.pkl",
        ],
        env="ENSEMBLE_MODEL_PATHS",
    )

    # Trading Configuration
    confidence_threshold: float = Field(default=60.0, env="CONFIDENCE_THRESHOLD")
    base_quantity: int = Field(default=100, env="BASE_QUANTITY")
    max_quantity: int = Field(default=500, env="MAX_QUANTITY")
    cycle_interval: int = Field(default=60, env="CYCLE_INTERVAL")

    # Portfolio Configuration
    initial_cash: float = Field(default=100000.0, env="INITIAL_CASH")
    max_position_percent: float = Field(default=0.20, env="MAX_POSITION_PERCENT")

    # Risk Management
    risk_multiplier_low: float = Field(default=1.2, env="RISK_MULTIPLIER_LOW")
    risk_multiplier_high: float = Field(default=0.5, env="RISK_MULTIPLIER_HIGH")

    # Database Configuration
    database_url: str = Field(default="sqlite:///./stockai.db", env="DATABASE_URL")

    # Redis Configuration
    redis_host: str = Field(default="localhost", env="REDIS_HOST")
    redis_port: int = Field(default=6379, env="REDIS_PORT")
    redis_db: int = Field(default=0, env="REDIS_DB")

    # Logging Configuration
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_file: str = Field(default="logs/stockai.log", env="LOG_FILE")

    # External APIs
    news_api_key: Optional[str] = Field(default=None, env="NEWS_API_KEY")
    financial_data_api_key: Optional[str] = Field(
        default=None, env="FINANCIAL_DATA_API_KEY"
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """Get application settings (singleton pattern)."""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings


def reload_settings() -> Settings:
    """Reload settings from environment."""
    global _settings
    _settings = Settings()
    return _settings
