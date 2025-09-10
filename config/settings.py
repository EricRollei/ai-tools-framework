"""
AI Tools Framework: settings.py
Description: AI Tools Framework component
Author: Eric Hiss (GitHub: EricRollei)
Contact: [eric@historic.camera, eric@rollei.us]
Version: 1.0.0
Date: 2025-09-09
License: Dual License (Non-Commercial and Commercial Use)
Copyright (c) 2025 Eric Hiss. All rights reserved.

Dual License:
1. Non-Commercial Use: This software is licensed under the terms of the
   Creative Commons Attribution-NonCommercial 4.0 International License.
   To view a copy of this license, visit http://creativecommons.org/licenses/by-nc/4.0/
   
2. Commercial Use: For commercial use, a separate license is required.
   Please contact Eric Hiss at [eric@historic.camera, eric@rollei.us] for licensing options.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A 
PARTICULAR PURPOSE AND NONINFRINGEMENT.

Dependencies:
This code depends on several third-party libraries, each with its own license.
See LICENSE file for complete dependency information.

settings.py - Part of AI Tools Framework
A comprehensive productivity framework with 27 tools for Claude Desktop and LM Studio
"""

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