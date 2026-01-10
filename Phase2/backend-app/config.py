"""
Configuration management for environment variables
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    # Database settings
    database_url: str = os.getenv("DATABASE_URL", "")

    # Authentication settings
    jwt_algorithm: str = os.getenv("JWT_ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    jwt_secret_key: str = os.getenv("BETTER_AUTH_SECRET", "")  # Use BETTER_AUTH_SECRET for JWT key
    better_auth_secret: str = os.getenv("BETTER_AUTH_SECRET", "")
    better_auth_url: str = os.getenv("BETTER_AUTH_URL", "http://localhost:3000")

    # CORS settings
    cors_origins: str = os.getenv("CORS_ORIGINS", "http://localhost:3000")

    # Application settings
    app_name: str = os.getenv("APP_NAME", "Backend Development Environment API")
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"
    port: int = int(os.getenv("PORT", "8000"))

    class Config:
        env_file = ".env"
        extra = "allow"  # Allow extra fields to prevent validation errors

# Create a global settings instance
settings = Settings()