"""
Configuration Settings

Loads environment variables from .env
using Pydantic Settings.
"""

from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


# Root Project Directory
BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    """
    Application Settings
    """

    # ==========================
    # Project
    # ==========================
    PROJECT_NAME: str = Field(default="KnowledgeOS AI")
    PROJECT_VERSION: str = Field(default="1.0.0")
    ENVIRONMENT: str = Field(default="development")

    # ==========================
    # API Keys
    # ==========================
    OPENROUTER_API_KEY: str
    PAGEINDEX_API_KEY: str
    PAGEINDEX_BASE_URL: str
    LLM_PROVIDER: str = "openrouter"

    # ==========================
    # Database
    # ==========================
    DATABASE_URL: str

    # ==========================
    # Model
    # ==========================
    MODEL_NAME: str

    # ==========================
    # Directories
    # ==========================
    UPLOAD_DIR: str = "uploads"
    REPORT_DIR: str = "reports"

    # ==========================
    # Backend
    # ==========================
    HOST: str = "127.0.0.1"
    PORT: int = 8000

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )
    LLM_MODEL: str = "google/gemma-3-12b-it"

    LLM_TEMPERATURE: float = 0.3

    LLM_MAX_TOKENS: int = 1024
    PAGEINDEX_API_KEY: str
    PAGEINDEX_BASE_URL: str


settings = Settings()