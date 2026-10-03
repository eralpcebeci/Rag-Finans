from fastapi.testclient import TestClient

from rag.api.main import app
from rag.shared.config import Settings


def test_health_returns_status() -> None:
    res = TestClient(app).get("/health")
    assert res.status_code == 200
    assert res.json()["api"] == "up"


def test_settings_defaults() -> None:
    s = Settings()
    assert s.chunk_size > s.chunk_overlap
