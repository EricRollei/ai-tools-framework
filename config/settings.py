# config/settings.py
from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional
import os

class Settings(BaseSettings):
    """Application configuration"""

    # API Keys
    serper_api_key: Optional[str] = Field(None, env="SERPER_API_KEY")
    openai_api_key: Optional[str] = Field(None, env="OPENAI_API_KEY")

    # Email Configuration
    smtp_server: Optional[str] = Field(None, env="SMTP_SERVER")
    smtp_port: int = Field(587, env="SMTP_PORT")
    smtp_from_email: Optional[str] = Field(None, env="SMTP_FROM_EMAIL")
    smtp_username: Optional[str] = Field(None, env="SMTP_USERNAME")
    smtp_password: Optional[str] = Field(None, env="SMTP_PASSWORD")

    # Server Configuration
    host: str = Field("localhost", env="HOST")
    port: int = Field(8000, env="PORT")

    # Logging
    log_level: str = Field("INFO", env="LOG_LEVEL")

    # Tool Configuration
    max_retries: int = Field(3, env="MAX_RETRIES")
    timeout_seconds: int = Field(30, env="TIMEOUT_SECONDS")

    class Config:
        env_file = ".env"
        case_sensitive = False

# Get global settings instance
settings = Settings()