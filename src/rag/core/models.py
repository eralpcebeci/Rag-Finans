from pydantic import BaseModel, Field


class ChunkMetadata(BaseModel):
    company: str
    year: int
    source_file: str
    page: int | None = None
    section: str | None = None


class Chunk(BaseModel):
    id: str
    text: str
    metadata: ChunkMetadata


class RetrievedChunk(BaseModel):
    chunk: Chunk
    score: float = Field(description="Arama skoru (yüksek = daha alakalı)")


class Answer(BaseModel):
    text: str
    sources: list[RetrievedChunk]
