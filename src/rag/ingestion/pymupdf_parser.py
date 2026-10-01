from pathlib import Path

import pymupdf

from rag.core.exceptions import ParsingError
from rag.ingestion.base import Parser
from rag.ingestion.models import Element, ElementType, ParsedDocument


class PyMuPDFParser(Parser):
    """
    Baseline parser.

    Her sayfanın metin katmanını tek bir TEXT elementi olarak çıkarır.
    """

    name = "pymupdf"

    def parse(self, path: Path) -> ParsedDocument:
        if not path.is_file():
            raise ParsingError(f"Dosya bulunamadı: {path}")

        elements: list[Element] = []

        with pymupdf.open(path) as doc:
            page_count = len(doc)

            for page_number, page in enumerate(doc, start=1):
                element = Element(
                    type=ElementType.TEXT,
                    page=page_number,
                    text=page.get_text("text"),
                    source=self.name,
                )

                elements.append(element)

        return ParsedDocument(
            source_file=path.name,
            parser=self.name,
            page_count=page_count,
            elements=elements,
        )
