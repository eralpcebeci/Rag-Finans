import pytest
from pydantic import ValidationError

from rag.ingestion.models import (
    BBox,
    Element,
    ElementType,
    ParsedDocument,
)


def make_element(
    *,
    page: int = 1,
    text: str = "örnek metin",
    source: str = "test",
    element_type: ElementType = ElementType.TEXT,
    bbox: BBox | None = None,
) -> Element:
    """Testlerde geçerli Element üretmek için yardımcı factory."""
    return Element(
        type=element_type,
        page=page,
        text=text,
        source=source,
        bbox=bbox,
    )


def make_document(
    *,
    elements: list[Element] | None = None,
    page_count: int = 2,
    source_file: str = "rapor.pdf",
    parser: str = "test",
) -> ParsedDocument:
    """Testlerde geçerli ParsedDocument üretmek için yardımcı factory."""
    return ParsedDocument(
        source_file=source_file,
        parser=parser,
        page_count=page_count,
        elements=elements or [],
    )


# ---------------------------------------------------------------------------
# ElementType
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("raw_value", "expected"),
    [
        ("text", ElementType.TEXT),
        ("heading", ElementType.HEADING),
        ("table", ElementType.TABLE),
        ("figure", ElementType.FIGURE),
        ("header_footer", ElementType.HEADER_FOOTER),
    ],
)
def test_element_accepts_supported_element_types(
    raw_value: str,
    expected: ElementType,
) -> None:
    element = Element(
        type=raw_value,
        page=1,
        text="test",
        source="test",
    )

    assert element.type == expected


def test_element_rejects_unknown_element_type() -> None:
    with pytest.raises(ValidationError):
        Element(
            type="chart",
            page=1,
            text="test",
            source="test",
        )


# ---------------------------------------------------------------------------
# Element.page
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("invalid_page", [0, -1, -100])
def test_element_page_must_start_from_one(invalid_page: int) -> None:
    with pytest.raises(ValidationError):
        make_element(page=invalid_page)


def test_element_accepts_positive_page_number() -> None:
    element = make_element(page=900)

    assert element.page == 900


# ---------------------------------------------------------------------------
# Element.text
# ---------------------------------------------------------------------------


def test_element_allows_empty_text() -> None:
    """
    Boş text her zaman parsing hatası değildir.

    Örneğin görsel ağırlıklı, kapak veya text layer'ı bulunmayan
    bölgelerde boş içerik oluşabilir.
    """
    element = make_element(text="")

    assert element.text == ""


def test_element_preserves_text_content() -> None:
    text = "Hasılat\n2025: 1.250.000 TL"

    element = make_element(text=text)

    assert element.text == text


# ---------------------------------------------------------------------------
# Element.source
# ---------------------------------------------------------------------------


def test_element_source_cannot_be_empty() -> None:
    with pytest.raises(ValidationError):
        make_element(source="")


def test_element_preserves_source() -> None:
    element = make_element(source="pymupdf")

    assert element.source == "pymupdf"


# ---------------------------------------------------------------------------
# Element.bbox
# ---------------------------------------------------------------------------


def test_element_allows_missing_bbox() -> None:
    element = make_element(bbox=None)

    assert element.bbox is None


def test_element_accepts_valid_bbox() -> None:
    bbox: BBox = (10.0, 20.0, 300.0, 400.0)

    element = make_element(bbox=bbox)

    assert element.bbox == bbox


@pytest.mark.parametrize(
    "invalid_bbox",
    [
        (10.0, 20.0, 30.0),
        (10.0, 20.0, 30.0, 40.0, 50.0),
    ],
)
def test_element_bbox_must_have_exactly_four_coordinates(
    invalid_bbox: tuple[float, ...],
) -> None:
    with pytest.raises(ValidationError):
        Element(
            type=ElementType.TEXT,
            page=1,
            text="test",
            source="test",
            bbox=invalid_bbox,
        )


# ---------------------------------------------------------------------------
# ParsedDocument metadata
# ---------------------------------------------------------------------------


def test_document_source_file_cannot_be_empty() -> None:
    with pytest.raises(ValidationError):
        make_document(source_file="")


def test_document_parser_cannot_be_empty() -> None:
    with pytest.raises(ValidationError):
        make_document(parser="")


@pytest.mark.parametrize("invalid_page_count", [-1, -10])
def test_document_page_count_cannot_be_negative(
    invalid_page_count: int,
) -> None:
    with pytest.raises(ValidationError):
        make_document(page_count=invalid_page_count)


def test_document_allows_zero_pages_when_empty() -> None:
    document = make_document(
        page_count=0,
        elements=[],
    )

    assert document.page_count == 0
    assert document.elements == []


# ---------------------------------------------------------------------------
# ParsedDocument element/page consistency
# ---------------------------------------------------------------------------


def test_document_accepts_element_on_last_page() -> None:
    document = make_document(
        page_count=900,
        elements=[
            make_element(page=900),
        ],
    )

    assert document.elements[0].page == 900


def test_document_rejects_element_beyond_page_count() -> None:
    with pytest.raises(ValidationError):
        make_document(
            page_count=10,
            elements=[
                make_element(page=11),
            ],
        )


def test_zero_page_document_rejects_elements() -> None:
    with pytest.raises(ValidationError):
        make_document(
            page_count=0,
            elements=[
                make_element(page=1),
            ],
        )


def test_document_validates_all_elements_against_page_count() -> None:
    elements = [
        make_element(page=1, text="bir"),
        make_element(page=2, text="iki"),
        make_element(page=50, text="geçersiz"),
    ]

    with pytest.raises(ValidationError):
        make_document(
            page_count=10,
            elements=elements,
        )


# ---------------------------------------------------------------------------
# ParsedDocument.elements
# ---------------------------------------------------------------------------


def test_document_creates_empty_element_list_by_default() -> None:
    document = ParsedDocument(
        source_file="rapor.pdf",
        parser="test",
        page_count=2,
    )

    assert document.elements == []


def test_documents_do_not_share_default_element_list() -> None:
    first = ParsedDocument(
        source_file="a.pdf",
        parser="test",
        page_count=1,
    )

    second = ParsedDocument(
        source_file="b.pdf",
        parser="test",
        page_count=1,
    )

    first.elements.append(make_element())

    assert len(first.elements) == 1
    assert second.elements == []


# ---------------------------------------------------------------------------
# ParsedDocument.page_text
# ---------------------------------------------------------------------------


def test_page_text_joins_only_elements_from_requested_page() -> None:
    document = make_document(
        page_count=2,
        elements=[
            make_element(page=1, text="birinci"),
            make_element(page=2, text="ikinci sayfa"),
            make_element(page=1, text="üçüncü"),
        ],
    )

    assert document.page_text(1) == "birinci\nüçüncü"


def test_page_text_preserves_element_order() -> None:
    document = make_document(
        page_count=1,
        elements=[
            make_element(page=1, text="başlık"),
            make_element(page=1, text="paragraf"),
            make_element(page=1, text="tablo"),
        ],
    )

    assert document.page_text(1) == "başlık\nparagraf\ntablo"


def test_page_text_returns_empty_string_when_page_has_no_elements() -> None:
    document = make_document(
        page_count=3,
        elements=[
            make_element(page=1, text="bir"),
        ],
    )

    assert document.page_text(2) == ""


# ---------------------------------------------------------------------------
# Serialization
# ---------------------------------------------------------------------------


def test_document_survives_json_roundtrip() -> None:
    original = make_document(
        page_count=2,
        elements=[
            make_element(
                page=1,
                text="Finansal tablo",
                source="pymupdf",
                element_type=ElementType.TABLE,
                bbox=(10.0, 20.0, 300.0, 400.0),
            ),
            make_element(
                page=2,
                text="Açıklama",
                source="pymupdf",
            ),
        ],
    )

    serialized = original.model_dump_json()
    restored = ParsedDocument.model_validate_json(serialized)

    assert restored == original
