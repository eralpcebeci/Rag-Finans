from dataclasses import dataclass
from pathlib import Path

import fitz  # PyMuPDF'in import adı "fitz"

from rag.core.exceptions import ParsingError


@dataclass
class ParsedPage:
    page_number: int  # 1'den başlar, kaynak gösterirken kullanacağız
    text: str
    image_count: int = 0  # sayfadaki gömülü görsel sayısı


def parse_pdf(path: Path) -> list[ParsedPage]:
    if not path.exists():
        raise ParsingError(f"Dosya bulunamadı: {path}")

    pages: list[ParsedPage] = []
    with fitz.open(path) as doc:
        for index, page in enumerate(doc, start=1):
            pages.append(
                ParsedPage(
                    page_number=index,
                    text=page.get_text("text"),
                    image_count=len(page.get_images()),
                )
            )
    return pages
