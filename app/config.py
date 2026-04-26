from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from pydantic import Field


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    DATABASE_URL: str = Field(..., description="Database connection string")
    SECRET_KEY: str = "changeme"
    DEBUG: bool = True


@lru_cache()
def get_settings() -> Settings:
    return Settings()
