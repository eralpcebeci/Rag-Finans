from fastapi import FastAPI
from qdrant_client import QdrantClient

from rag.core.config import get_settings
from rag.core.logging import setup_logging

settings = get_settings()
setup_logging(settings.log_level)

app = FastAPI(title="RAG Finans", version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    """API ve Qdrant bağlantısını kontrol eder."""
    try:
        QdrantClient(url=settings.qdrant_url, timeout=2).get_collections()
        qdrant = "up"
    except Exception:
        qdrant = "down"
    return {"api": "up", "qdrant": qdrant, "env": settings.app_env}
