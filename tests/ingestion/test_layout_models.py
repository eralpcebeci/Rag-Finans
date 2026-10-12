import pytest
from pydantic import ValidationError

from rag.modules.ingestion.domain.layout_models import LayoutLine, LayoutSpan


def test_layout_span_accepts_valid_layout_data() -> None:
    span = LayoutSpan(
        text="Sermaye Yeterliliği",
        page=21,
        bbox=(72.0, 120.0, 250.0, 140.0),
        font_size=2.3,
        font_name="Test Span",
        is_bold=True,
    )

    assert span.text == "Sermaye Yeterliliği"
    assert span.page == 21
    assert span.font_size == 2.3
    assert span.is_bold is True


def test_layout_span_rejects_empty_text() -> None:
    with pytest.raises(ValidationError):
        LayoutSpan(
            text="",
            page=30,
            bbox=(23.1, 43.2, 53.1, 55.7),
            font_size=4,
            font_name="Arial",
            is_bold=False,
        )


def test_layout_span_rejects_invalid_page() -> None:
    with pytest.raises(ValidationError):
        LayoutSpan(
            text="abc",
            page=0,
            bbox=(23.1, 43.2, 53.1, 55.7),
            font_size=4,
            font_name="Arial",
            is_bold=False,
        )


def test_layout_span_rejects_non_positive_font_size() -> None:
    with pytest.raises(ValidationError):
        LayoutSpan(
            text="abc",
            page=5,
            bbox=(44.3, 32.3, 44.1, 99.4),
            font_size=0,
            font_name="Arial",
            is_bold=True,
        )


def test_layout_span_rejects_empty_font_name() -> None:
    with pytest.raises(ValidationError):
        LayoutSpan(
            text="abc",
            page=5,
            bbox=(32.1, 123.5, 234.1, 33.3),
            font_size=1,
            font_name="",
            is_bold=False,
        )


def test_layout_span_rejects_invalid_bbox_length() -> None:
    with pytest.raises(ValidationError):
        LayoutSpan(
            text="abc",
            page=23,
            bbox=(321.3, 32.1, 66.8),
            font_size=5,
            font_name="Arial Black",
            is_bold=False,
        )


def test_layout_span_rejects_bbox_with_reversed_x_coordinates() -> None:
    with pytest.raises(ValidationError):
        LayoutSpan(
            text="abc",
            page=55,
            bbox=(80.3, 32.3, 50.3, 40.6),
            font_size=124,
            font_name="Times New Roman",
            is_bold=True,
        )


def test_layout_span_rejects_bbox_with_reversed_y_coordinates() -> None:
    with pytest.raises(ValidationError):
        LayoutSpan(
            text="abc",
            page=43,
            bbox=(20.0, 50.0, 80.0, 32.3),
            font_size=96,
            font_name="Times New Roman",
            is_bold=True,
        )


def test_layout_line_derives_properties_from_spans() -> None:
    span_1 = LayoutSpan(
        text="Sermaye ",
        page=1,
        bbox=(10.0, 20.0, 50.0, 40.0),
        font_size=12.0,
        font_name="Campton-Book",
        is_bold=False,
    )

    span_2 = LayoutSpan(
        text="Yeterliliği",
        page=1,
        bbox=(50.0, 20.0, 100.0, 40.0),
        font_size=18.0,
        font_name="Campton-Bold",
        is_bold=True,
    )

    line = LayoutLine(
        spans=[span_1, span_2],
    )

    assert line.text == "Sermaye Yeterliliği"
    assert line.page == 1
    assert line.max_font_size == 18.0
    assert line.is_bold is True
    assert line.bbox == (10.0, 20.0, 100.0, 40.0)


def test_layout_line_rejects_spans_from_different_pages() -> None:
    span_1 = LayoutSpan(
        text="Sermaye ",
        page=1,
        bbox=(10.0, 20.0, 50.0, 40.0),
        font_size=12.0,
        font_name="Campton-Book",
        is_bold=False,
    )

    span_2 = LayoutSpan(
        text="Yeterliliği",
        page=2,
        bbox=(50.0, 20.0, 100.0, 40.0),
        font_size=18.0,
        font_name="Campton-Bold",
        is_bold=True,
    )

    with pytest.raises(ValidationError):
        LayoutLine(
            spans=[span_1, span_2],
        )
