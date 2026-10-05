from pathlib import Path

import pytest

from rag.modules.ingestion.domain.enums import ElementType
from rag.modules.ingestion.domain.models import ParsedDocument
from rag.modules.ingestion.exceptions import ParsingError
from rag.modules.ingestion.infrastructure.parsers.pymupdf_parser import (
    PyMuPDFParser,
)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
REPORT_PATH = PROJECT_ROOT / "data" / "raw" / "akbank_2025_faaliyet.pdf"


def test_pymupdf_parser_parses_real_akbank_report() -> None:
    assert REPORT_PATH.is_file(), f"Test PDF'i bulunamadı: {REPORT_PATH}"

    result = PyMuPDFParser().parse(REPORT_PATH)

    assert isinstance(result, ParsedDocument)

    assert result.source_file == "akbank_2025_faaliyet.pdf"
    assert result.parser == "pymupdf"

    assert result.page_count > 0
    assert len(result.elements) == result.page_count

    assert result.elements[0].page == 1
    assert result.elements[-1].page == result.page_count

    assert all(element.type == ElementType.TEXT for element in result.elements)

    assert all(element.source == "pymupdf" for element in result.elements)

    assert any(element.text.strip() for element in result.elements)


def test_pymupdf_parser_rejects_missing_file(tmp_path: Path) -> None:
    missing_pdf = tmp_path / "olmayan.pdf"

    with pytest.raises(ParsingError):
        PyMuPDFParser().parse(missing_pdf)
