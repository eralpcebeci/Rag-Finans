from rag.shared.exceptions import RagError


class IngestionError(RagError):
    """Ingestion modülündeki hataların ortak tabanı."""


class ParsingError(IngestionError):
    """Bir doküman ayrıştırılamadığında oluşan hata."""
