"""
PAMS Configuration Settings
"""
import os
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # API Settings
    API_TITLE: str = "PAMS - Product Alert Management System"
    API_VERSION: str = "1.0.0"
    API_DESCRIPTION: str = "AI-driven Product Alert Management with Predictive Analytics"
    
    # Database
    DATABASE_URL: str = "postgresql+psycopg2://user:pass@localhost:5432/pams"
    DATABASE_ECHO: bool = False
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    CORS_ORIGINS: list = ["http://localhost:3000", "http://localhost:8000"]
    
    # ML Model Settings
    ML_MODEL_PATH: str = "./ml_models"
    ML_ENABLE_GPU: bool = False
    ML_BATCH_SIZE: int = 32
    
    # Alert Settings
    ALERT_DEDUPLICATION_THRESHOLD: float = 0.8
    ALERT_SLA_P1_HOURS: int = 4
    ALERT_SLA_P2_HOURS: int = 24
    ALERT_SLA_P3_HOURS: int = 72
    ALERT_SLA_P4_HOURS: int = 168
    
    # Notification Settings
    ENABLE_EMAIL_NOTIFICATIONS: bool = True
    ENABLE_SMS_NOTIFICATIONS: bool = False
    ENABLE_PUSH_NOTIFICATIONS: bool = True
    
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    SMTP_FROM_EMAIL: Optional[str] = None
    
    TWILIO_ACCOUNT_SID: Optional[str] = None
    TWILIO_AUTH_TOKEN: Optional[str] = None
    TWILIO_PHONE_NUMBER: Optional[str] = None
    
    # Celery (Background Tasks)
    CELERY_BROKER_URL: str = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/2"
    
    # Monitoring
    SENTRY_DSN: Optional[str] = None
    ENABLE_PROMETHEUS: bool = True
    
    # Feature Flags
    ENABLE_ADVANCED_ML: bool = True
    ENABLE_REAL_TIME_PROCESSING: bool = True
    ENABLE_AUTO_ESCALATION: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
