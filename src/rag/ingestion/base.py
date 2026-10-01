from abc import ABC, abstractmethod
from pathlib import Path

from rag.ingestion.models import ParsedDocument


class Parser(ABC):
    """Her PDF ayrıştırıcısının uyması gereken sözleşme."""

    name: str

    @abstractmethod
    def parse(self, path: Path) -> ParsedDocument:
        """
        Dosyayı okuyup ParsedDocument döndürür.

        Parser kaynak içeriği sessizce değiştirmemeli veya atmamalıdır.
        """
        raise NotImplementedError
