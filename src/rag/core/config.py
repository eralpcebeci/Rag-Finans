from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Tüm ayarlar .env veya ortam değişkenlerinden (RAG_ öneki) okunur."""

    model_config = SettingsConfigDict(env_file=".env", env_prefix="RAG_", extra="ignore")

    app_env: str = "dev"
    log_level: str = "INFO"

    qdrant_url: str = "http://localhost:6333"
    qdrant_collection: str = "kap_reports"

    # Deney parametreleri
    parser: str = "pymupdf"
    chunk_size: int = 800
    chunk_overlap: int = 100
    embedding_model: str = "BAAI/bge-m3"
    llm_provider: str = "anthropic"
    llm_model: str = ""
    llm_api_key: str = ""


@lru_cache
def get_settings() -> Settings:
    return Settings()
