import pytest
from pydantic import ValidationError

from rag.modules.ingestion.domain.enums import DecisionStatus, LineRole
from rag.modules.ingestion.domain.heading_models import HeadingDecision, LineSignals
from rag.modules.ingestion.domain.layout_models import LayoutLine, LayoutSpan


def test_line_signals_accepts_valid_values() -> None:
    signals = LineSignals(
        font_size_ratio=1.5,
        is_bold=True,
        char_count=22,
        word_count=3,
        ends_with_terminal_punctuation=False,
        starts_with_numbering=True,
    )

    assert signals.font_size_ratio == 1.5
    assert signals.is_bold is True
    assert signals.char_count == 22
    assert signals.word_count == 3
    assert signals.ends_with_terminal_punctuation is False
    assert signals.starts_with_numbering is True


def test_line_signals_rejects_non_positive_font_size_ratio() -> None:
    with pytest.raises(ValidationError):
        LineSignals(
            font_size_ratio=0,
            is_bold=True,
            char_count=22,
            word_count=3,
            ends_with_terminal_punctuation=False,
            starts_with_numbering=True,
        )


def test_line_signals_rejects_non_positive_char_count() -> None:
    with pytest.raises(ValidationError):
        LineSignals(
            font_size_ratio=1.5,
            is_bold=True,
            char_count=0,
            word_count=3,
            ends_with_terminal_punctuation=False,
            starts_with_numbering=True,
        )


def test_line_signals_rejects_non_positive_word_count() -> None:
    with pytest.raises(ValidationError):
        LineSignals(
            font_size_ratio=1.5,
            is_bold=True,
            char_count=22,
            word_count=0,
            ends_with_terminal_punctuation=False,
            starts_with_numbering=True,
        )


def test_heading_decision_accepts_valid_values() -> None:
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

    signals = LineSignals(
        font_size_ratio=1.5,
        is_bold=True,
        char_count=14,
        word_count=2,
        ends_with_terminal_punctuation=False,
        starts_with_numbering=False,
    )

    decision = HeadingDecision(
        line=line,
        signals=signals,
        heading_score=1.3,
        text_score=0.2,
        role=LineRole.HEADING_CANDIDATE,
        status=DecisionStatus.CONFIDENT,
    )

    assert decision.line == line
    assert decision.signals == signals
    assert decision.heading_score == 1.3
    assert decision.text_score == 0.2
    assert decision.role == LineRole.HEADING_CANDIDATE
    assert decision.status == DecisionStatus.CONFIDENT


def test_heading_decision_rejects_negative_heading_score() -> None:
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

    signals = LineSignals(
        font_size_ratio=1.5,
        is_bold=True,
        char_count=14,
        word_count=2,
        ends_with_terminal_punctuation=False,
        starts_with_numbering=False,
    )

    with pytest.raises(ValidationError):
        HeadingDecision(
            line=line,
            signals=signals,
            heading_score=-0.1,
            text_score=0.2,
            role=LineRole.HEADING_CANDIDATE,
            status=DecisionStatus.CONFIDENT,
        )


def test_heading_decision_rejects_negative_text_score() -> None:
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

    signals = LineSignals(
        font_size_ratio=1.5,
        is_bold=True,
        char_count=14,
        word_count=2,
        ends_with_terminal_punctuation=False,
        starts_with_numbering=False,
    )

    with pytest.raises(ValidationError):
        HeadingDecision(
            line=line,
            signals=signals,
            heading_score=1.3,
            text_score=-0.2,
            role=LineRole.HEADING_CANDIDATE,
            status=DecisionStatus.CONFIDENT,
        )
