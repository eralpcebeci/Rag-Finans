from fastapi import FastAPI
from qdrant_client import QdrantClient

from rag.shared.config import get_settings
from rag.shared.logging import setup_logging

settings = get_settings()
setup_logging(settings.log_level)

app = FastAPI(
    title="RAG Finans",
    version="0.1.0",
)


@app.get("/health")
def health() -> dict[str, str]:
    """API ve Qdrant bağlantısının durumunu döndürür."""

    try:
        QdrantClient(
            url=settings.qdrant_url,
            timeout=2,
        ).get_collections()

        qdrant_status = "up"
    except Exception:
        qdrant_status = "down"

    return {
        "api": "up",
        "qdrant": qdrant_status,
        "env": settings.app_env,
    }
