from pydantic import BaseModel, Field

from rag.modules.ingestion.domain.enums import DecisionStatus, LineRole
from rag.modules.ingestion.domain.layout_models import LayoutLine


class LineSignals(BaseModel):
    """Bir LayoutLine için çıkarılan heading/text karar sinyalleri."""

    font_size_ratio: float = Field(
        gt=0,
        description="Satır font boyutunun body font boyutuna oranı.",
    )

    is_bold: bool

    char_count: int = Field(
        ge=1,
        description="Satırdaki karakter sayısı.",
    )

    word_count: int = Field(
        ge=1,
        description="Satırdaki kelime sayısı.",
    )

    ends_with_terminal_punctuation: bool

    starts_with_numbering: bool


class HeadingDecision(BaseModel):
    """
    Bir LayoutLine için çıkarılan sinyalleri, skorları
    ve nihai heading/text sınıflandırma kararını temsil eder.
    """

    line: LayoutLine

    signals: LineSignals

    heading_score: float = Field(
        ge=0,
        description="Satırın heading olması lehindeki evidence skoru.",
    )

    text_score: float = Field(
        ge=0,
        description="Satırın normal metin olması lehindeki evidence skoru.",
    )

    role: LineRole

    status: DecisionStatus
