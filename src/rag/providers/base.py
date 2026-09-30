"""Sağlayıcı arayüzleri. Model/DB değiştirmek = yeni bir sınıf yazmak."""

from abc import ABC, abstractmethod

from rag.core.models import Chunk, RetrievedChunk


class Embedder(ABC):
    @property
    @abstractmethod
    def dimension(self) -> int: ...

    @abstractmethod
    def embed_documents(self, texts: list[str]) -> list[list[float]]: ...

    @abstractmethod
    def embed_query(self, text: str) -> list[float]: ...


class VectorStore(ABC):
    @abstractmethod
    def upsert(self, chunks: list[Chunk], vectors: list[list[float]]) -> None: ...

    @abstractmethod
    def search(
        self, vector: list[float], top_k: int = 5, filters: dict[str, object] | None = None
    ) -> list[RetrievedChunk]: ...


class LLM(ABC):
    @abstractmethod
    def generate(self, prompt: str, system: str | None = None) -> str: ...
