from abc import ABC, abstractmethod
from pathlib import Path

from rag.modules.ingestion.domain.models import ParsedDocument


class Parser(ABC):
    """Her doküman parser'ının uyması gereken sözleşme."""

    name: str

    @abstractmethod
    def parse(self, path: Path) -> ParsedDocument:
        """
        Verilen dosyayı ayrıştırıp normalize edilmiş ParsedDocument döndürür.

        Parser, kaynak içeriği sessizce değiştirmemeli veya atmamalıdır.
        """
        raise NotImplementedError
