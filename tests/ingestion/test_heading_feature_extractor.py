import pytest

from rag.modules.ingestion.application.heading.feature_extractor import HeadingFeatureExtractor
from rag.modules.ingestion.domain.layout_models import LayoutLine, LayoutSpan


def test_heading_feature_extractor_extracts_signals_from_layout_line() -> None:
    span = LayoutSpan(
        text="Risk Yönetimi",
        page=1,
        bbox=(10.0, 20.0, 100.0, 40.0),
        font_size=18.0,
        font_name="Campton-Bold",
        is_bold=True,
    )

    line = LayoutLine(
        spans=[span],
    )

    extractor = HeadingFeatureExtractor()

    signals = extractor.extract(
        line=line,
        body_font_size=9.0,
    )
    assert signals.font_size_ratio == 2.0
    assert signals.is_bold is True
    assert signals.char_count == 13
    assert signals.word_count == 2
    assert signals.ends_with_terminal_punctuation is False
    assert signals.starts_with_numbering is False


def test_heading_feature_extractor_rejects_non_positive_body_font_size() -> None:
    span = LayoutSpan(
        text="Risk Yönetimi",
        page=1,
        bbox=(10.0, 20.0, 100.0, 40.0),
        font_size=18.0,
        font_name="Campton-Bold",
        is_bold=True,
    )

    line = LayoutLine(
        spans=[span],
    )

    extractor = HeadingFeatureExtractor()

    with pytest.raises(ValueError):
        extractor.extract(
            line=line,
            body_font_size=-9.0,
        )


def test_heading_feature_extractor_detects_numbered_heading_pattern() -> None:
    span = LayoutSpan(
        text="3.2 Risk Yönetimi",
        page=1,
        bbox=(10.0, 20.0, 100.0, 40.0),
        font_size=18.0,
        font_name="Campton-Bold",
        is_bold=True,
    )

    line = LayoutLine(
        spans=[span],
    )

    extractor = HeadingFeatureExtractor()

    signals = extractor.extract(
        line=line,
        body_font_size=9.0,
    )

    assert signals.starts_with_numbering is True


def test_heading_feature_extractor_detects_terminal_punctuation() -> None:
    span = LayoutSpan(
        text="Bankanın aktifleri artmıştır.",
        page=1,
        bbox=(10.0, 20.0, 100.0, 40.0),
        font_size=18.0,
        font_name="Campton-Bold",
        is_bold=True,
    )

    line = LayoutLine(
        spans=[span],
    )

    extractor = HeadingFeatureExtractor()

    signals = extractor.extract(
        line=line,
        body_font_size=9.0,
    )

    assert signals.ends_with_terminal_punctuation is True
