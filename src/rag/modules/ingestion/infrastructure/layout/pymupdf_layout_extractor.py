from pathlib import Path

import pymupdf

from rag.modules.ingestion.domain.layout_models import LayoutLine, LayoutSpan
from rag.modules.ingestion.exceptions import ParsingError
from rag.modules.ingestion.ports.layout_extractor import LayoutExtractor


class PyMuPDFLayoutExtractor(LayoutExtractor):
    """PyMuPDF tabanlı canonical layout extractor."""

    def extract(self, path: Path) -> list[LayoutLine]:
        if not path.is_file():
            raise ParsingError(f"Dosya bulunamadı: {path}")

        lines: list[LayoutLine] = []

        with pymupdf.open(path) as doc:
            for page_number, page in enumerate(doc, start=1):
                page_dict = page.get_text("dict")

                for block in page_dict.get("blocks", []):
                    for line in block.get("lines", []):
                        line_spans: list[LayoutSpan] = []

                        for raw_span in line.get("spans", []):
                            raw_text = raw_span.get("text", "")

                            if not raw_text.strip():
                                continue

                            layout_span = LayoutSpan(
                                text=raw_text,
                                page=page_number,
                                bbox=tuple(raw_span["bbox"]),
                                font_size=float(raw_span["size"]),
                                font_name=raw_span["font"],
                                is_bold=bool(raw_span.get("flags", 0) & pymupdf.TEXT_FONT_BOLD),
                            )

                            line_spans.append(layout_span)

                        if line_spans:
                            lines.append(
                                LayoutLine(
                                    spans=line_spans,
                                )
                            )

        return lines
