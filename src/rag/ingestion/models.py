from dataclasses import dataclass, field
from enum import Enum

BBox = tuple[float, float, float, float]  # (x0, y0, x1, y1), sayfa koordinatları


class ElementType(str, Enum):
    TEXT = "text"
    HEADING = "heading"
    TABLE = "table"
    FIGURE = "figure"
    HEADER_FOOTER = "header_footer"


@dataclass(frozen=True)
class Element:
    """Bir sayfadaki tek bir içerik parçası."""

    type: ElementType
    page: int  # 1'den başlar
    text: str
    source: str  # bu parçayı hangi parser üretti
    bbox: BBox | None = None


@dataclass
class ParsedDocument:
    source_file: str
    parser: str
    page_count: int
    elements: list[Element] = field(default_factory=list)

    def page_text(self, page: int) -> str:
        """Bir sayfadaki tüm elementlerin metnini sırayla birleştirir."""
        return "\n".join(e.text for e in self.elements if e.page == page)
