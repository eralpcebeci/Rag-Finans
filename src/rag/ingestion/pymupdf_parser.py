from pathlib import Path

import pymupdf

from rag.core.exceptions import ParsingError
from rag.ingestion.base import Parser
from rag.ingestion.models import Element, ElementType, ParsedDocument


class PyMuPDFParser(Parser):
    """Baseline: her sayfanın metin katmanını olduğu gibi tek bir TEXT elementi yapar."""

    name = "pymupdf"

    def parse(self, path: Path) -> ParsedDocument:
        if not path.exists():
            raise ParsingError(f"Dosya bulunamadı:{path}")

        with pymupdf.open(path) as doc:
            result = ParsedDocument(
                source_file=path.name,
                parser=self.name,
                page_count=len(doc),
            )
            for number, page in enumerate(doc, start=1):
                result.elements.append(
                    Element(
                        type=ElementType.TEXT,
                        page=number,
                        text=page.get_text("text"),
                        source=self.name,
                    )
                )
            return result
