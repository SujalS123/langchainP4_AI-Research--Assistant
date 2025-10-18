"""
Configuration settings for the AI Research Assistant.
"""

from datetime import datetime
from pydantic_settings import BaseSettings
from functools import lru_cache
import os


class Settings(BaseSettings):
    """Application settings"""
    
    # API Keys
    GOOGLE_API_KEY: str  # Used for Gemini API
    SERPER_API_KEY: str | None = None  # Optional
    LANGCHAIN_API_KEY: str | None = None  # Optional, for LangSmith
    LANGCHAIN_ENDPOINT: str = "https://api.smith.langchain.com"  # LangSmith endpoint
    
    # Application Settings
    APP_NAME: str = "AI Research Assistant"
    DEBUG: bool = False
    
    @property
    def GEMINI_API_KEY(self) -> str:
        """Alias for GOOGLE_API_KEY since we're using it for Gemini"""
        return self.GOOGLE_API_KEY
    
    # Server settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    ENVIRONMENT: str = "development"
    
    # CORS
    ALLOWED_ORIGINS: str = "http://localhost:3000,http://localhost:5173"
    
    # Model Settings
    DEFAULT_MODEL: str = "gemini-pro"
    DEFAULT_TEMPERATURE: float = 0.7
    MAX_TOKENS: int = 1000
    
    # Cache Settings
    REDIS_URL: str | None = None
    CACHE_TTL_HOURS: int = 24
    
    # Search settings
    MAX_SEARCH_RESULTS: int = 10
    SEARCH_TIMEOUT: int = 30
    
    @staticmethod
    def get_current_time() -> str:
        """Get current timestamp in ISO format"""
        return datetime.now().isoformat()
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "allow"  # Allow extra fields in the settings


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()


# Create settings instance
settings = get_settings()

# Validate required settings
if not settings.GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY must be set in environment or .env file (used for Gemini API)")