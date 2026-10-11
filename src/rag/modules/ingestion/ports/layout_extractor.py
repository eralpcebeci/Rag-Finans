from abc import ABC, abstractmethod
from pathlib import Path

from rag.modules.ingestion.domain.layout_models import LayoutLine


class LayoutExtractor(ABC):
    """PDF'den canonical layout satırlarını çıkaran port."""

    @abstractmethod
    def extract(self, path: Path) -> list[LayoutLine]:
        """
        Verilen PDF dosyasından canonical layout satırlarını çıkarır.

        Args:
            path: İşlenecek PDF dosyasının yolu.

        Returns:
            Canonical LayoutLine nesnelerinden oluşan liste.
        """
        ...
