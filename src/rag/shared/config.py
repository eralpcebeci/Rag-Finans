from functools import lru_cache

from pydantic import Field, SecretStr, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Uygulama ayarlarını .env ve ortam değişkenlerinden yükler."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="RAG_",
        extra="ignore",
    )

    # Application
    app_env: str = "dev"
    log_level: str = "INFO"

    # Ingestion
    parser: str = "pymupdf"

    # Indexing
    chunk_size: int = Field(default=800, gt=0)
    chunk_overlap: int = Field(default=100, ge=0)
    embedding_model: str = "BAAI/bge-m3"

    # Vector store
    qdrant_url: str = "http://localhost:6333"
    qdrant_collection: str = "kap_reports"

    # Generation
    llm_provider: str = "ollama"
    llm_model: str = ""
    llm_api_key: SecretStr | None = None

    @model_validator(mode="after")
    def validate_chunking_settings(self) -> "Settings":
        if self.chunk_overlap >= self.chunk_size:
            raise ValueError("chunk_overlap, chunk_size değerinden küçük olmalıdır.")

        return self


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
