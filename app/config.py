"""Application configuration and environment variables"""

from functools import lru_cache
from typing import Optional, List
from pydantic_settings import BaseSettings
from pydantic import Field
import os


class Settings(BaseSettings):
    """Application settings from environment variables"""

    # ============================================
    # Application Settings
    # ============================================
    APP_NAME: str = Field(default="Battery-Twin-MVP")
    APP_VERSION: str = Field(default="1.0.0")
    DEBUG: bool = Field(default=False)
    ENVIRONMENT: str = Field(default="production")
    LOG_LEVEL: str = Field(default="INFO")

    # ============================================
    # Database Configuration
    # ============================================
    DATABASE_URL: str = Field(default="postgresql://user:password@localhost/battery_twin")
    DATABASE_POOL_SIZE: int = Field(default=20)
    DATABASE_MAX_OVERFLOW: int = Field(default=10)
    DATABASE_ECHO: bool = Field(default=False)

    # ============================================
    # JWT Authentication
    # ============================================
    SECRET_KEY: str = Field(default="dev-secret-key-change-in-production")
    ALGORITHM: str = Field(default="HS256")
    ACCESS_TOKEN_EXPIRY: int = Field(default=3600)  # 1 hour

    # ============================================
    # Redis Configuration (Optional)
    # ============================================
    REDIS_URL: Optional[str] = Field(default="redis://localhost:6379/0")
    USE_REDIS: bool = Field(default=False)

    # ============================================
    # Celery Configuration (Optional)
    # ============================================
    CELERY_BROKER_URL: Optional[str] = Field(default="redis://localhost:6379/0")
    CELERY_RESULT_BACKEND: Optional[str] = Field(default="redis://localhost:6379/1")
    USE_CELERY: bool = Field(default=False)

    # ============================================
    # ML Models Configuration
    # ============================================
    MODELS_PATH: str = Field(default="./app/models/ml")
    SOC_MODEL_NAME: str = Field(default="soc_model.pkl")
    SOH_MODEL_NAME: str = Field(default="soh_model.pkl")
    FORECAST_MODEL_NAME: str = Field(default="forecast_model.pkl")
    MODEL_INFERENCE_TIMEOUT: int = Field(default=5000)  # ms
    ENABLE_MOCK_MODELS: bool = Field(default=False)

    # ============================================
    # CORS Configuration
    # ============================================
    CORS_ORIGINS: List[str] = Field(default=["http://localhost:3000", "http://localhost:8000"])
    CORS_ALLOW_CREDENTIALS: bool = Field(default=True)
    CORS_ALLOW_METHODS: List[str] = Field(default=["*"])
    CORS_ALLOW_HEADERS: List[str] = Field(default=["*"])

    # ============================================
    # API Configuration
    # ============================================
    API_PORT: int = Field(default=8000)
    API_HOST: str = Field(default="0.0.0.0")
    API_WORKERS: int = Field(default=4)

    # ============================================
    # Anomaly Detection Thresholds
    # ============================================
    ANOMALY_SOH_THRESHOLD: float = Field(default=0.8)
    ANOMALY_RESISTANCE_THRESHOLD: float = Field(default=1.5)
    ANOMALY_VOLTAGE_RANGE: float = Field(default=3.0)
    ANOMALY_TEMPERATURE_RANGE: float = Field(default=60)

    # ============================================
    # Forecasting Parameters
    # ============================================
    FORECAST_HORIZON_HOURS: int = Field(default=24)
    FORECAST_STEP_SIZE: int = Field(default=1)
    FORECAST_CONFIDENCE_INTERVAL: float = Field(default=0.95)

    # ============================================
    # Feature Engineering Parameters
    # ============================================
    FEATURE_SMOOTHING_WINDOW: int = Field(default=5)
    FEATURE_NORMALIZATION: bool = Field(default=True)
    FEATURE_SCALING_METHOD: str = Field(default="standard")

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
