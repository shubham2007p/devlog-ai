import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    DATABASE_URL: str = "sqlite:///./database/database.db"
    WEBHOOK_SECRET: str = "local_webhook_secret_placeholder"
    GITHUB_TOKEN: str = "local_github_token_placeholder"
    GEMINI_API_KEY: str = "local_gemini_key_placeholder"

    # Support env_file configuration
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
