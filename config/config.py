import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, PostgresDsn, RedisDsn

class Settings(BaseSettings):
    # Core Environment
    ENVIRONMENT: str = Field(default="development")
    LOG_LEVEL: str = Field(default="INFO")
    
    # Infrastructure Connections
    DATABASE_URL: str = Field(
        default="postgresql+asyncpg://postgres:postgres@localhost:5432/website_agency"
    )
    REDIS_URL: str = Field(
        default="redis://localhost:6379/0"
    )
    
    # Third-Party Integrations
    GEMINI_API_KEY: str = Field(default="dummy_gemini_key")
    TELEGRAM_BOT_TOKEN: str = Field(default="dummy_token")
    TELEGRAM_CHAT_ID: str = Field(default="dummy_chat")
    
    # EDK Framework configuration
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
