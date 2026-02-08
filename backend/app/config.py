"""Application configuration using Pydantic settings."""

from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # OpenAI
    openai_api_key: str

    # Supabase
    supabase_url: str
    supabase_key: str
    supabase_service_key: str | None = None

    # App settings
    debug: bool = False
    cors_origins: str = "http://localhost:5173,http://localhost:3000,https://*.vercel.app"

    # Model settings
    embedding_model: str = "text-embedding-3-small"
    chat_model: str = "gpt-5.2"
    embedding_dimensions: int = 1536

    # RAG settings
    chunk_size: int = 1000
    chunk_overlap: int = 200
    retrieval_k: int = 4

    # Timeout settings (seconds) - tuned for Vercel hobby plan 10s limit
    agent_timeout: int = 8
    agent_max_steps: int = 6

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @property
    def cors_origins_list(self) -> list[str]:
        """Parse CORS origins from comma-separated string."""
        return [origin.strip() for origin in self.cors_origins.split(",")]


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
