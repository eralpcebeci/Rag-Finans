import re

from rag.modules.ingestion.domain.heading_models import LineSignals
from rag.modules.ingestion.domain.layout_models import LayoutLine


class HeadingFeatureExtractor:
    """LayoutLine üzerinden heading/text sınıflandırma sinyalleri üretir."""

    def extract(
        self,
        line: LayoutLine,
        body_font_size: float,
    ) -> LineSignals:
        if body_font_size <= 0:
            raise ValueError("body_font_size sıfırdan büyük olmalıdır.")

        text = line.text.strip()

        font_size_ratio = line.max_font_size / body_font_size
        is_bold = line.is_bold
        char_count = len(text)
        word_count = len(text.split())

        ends_with_terminal_punctuation = text.endswith((".", "?", "!"))

        starts_with_numbering = bool(
            re.match(
                r"^\d+(?:\.\d+)*[.)]?\s+",
                text,
            )
        )

        return LineSignals(
            font_size_ratio=font_size_ratio,
            is_bold=is_bold,
            char_count=char_count,
            word_count=word_count,
            ends_with_terminal_punctuation=ends_with_terminal_punctuation,
            starts_with_numbering=starts_with_numbering,
        )
