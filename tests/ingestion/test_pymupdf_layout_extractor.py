from pathlib import Path

import pytest

from rag.modules.ingestion.domain.layout_models import LayoutLine, LayoutSpan
from rag.modules.ingestion.exceptions import ParsingError
from rag.modules.ingestion.infrastructure.layout.pymupdf_layout_extractor import (
    PyMuPDFLayoutExtractor,
)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
REPORT_PATH = PROJECT_ROOT / "data" / "raw" / "akbank_2025_faaliyet.pdf"


def test_pymupdf_layout_extractor_rejects_missing_file(
    tmp_path: Path,
) -> None:
    missing_pdf = tmp_path / "olmayan.pdf"

    with pytest.raises(ParsingError):
        PyMuPDFLayoutExtractor().extract(missing_pdf)


def test_pymupdf_layout_extractor_extracts_layout_lines_from_real_report() -> None:
    assert REPORT_PATH.is_file(), f"Test PDF'i bulunamadı: {REPORT_PATH}"

    lines = PyMuPDFLayoutExtractor().extract(REPORT_PATH)

    assert lines

    assert all(isinstance(line, LayoutLine) for line in lines)

    assert all(line.page >= 1 for line in lines)

    assert all(line.text for line in lines)

    assert all(line.max_font_size > 0 for line in lines)

    assert all(line.spans for line in lines)

    assert all(isinstance(span, LayoutSpan) for line in lines for span in line.spans)
