from enum import Enum

from pydantic import BaseModel, Field, model_validator

BBox = tuple[float, float, float, float]
# (x0, y0, x1, y1) -> sayfa üzerindeki dikdörtgen bölgenin koordinatları


class ElementType(str, Enum):
    TEXT = "text"
    HEADING = "heading"
    TABLE = "table"
    FIGURE = "figure"
    HEADER_FOOTER = "header_footer"


class Element(BaseModel):
    """Bir sayfadaki tek bir içerik parçası."""

    type: ElementType

    page: int = Field(
        ge=1,
        description="Elementin bulunduğu sayfa numarası. 1'den başlar.",
    )

    text: str

    source: str = Field(
        min_length=1,
        description="Bu elementi üreten parser veya reader.",
    )

    bbox: BBox | None = None


class ParsedDocument(BaseModel):
    """Bir parser'ın ürettiği normalize edilmiş doküman."""

    source_file: str = Field(min_length=1)

    parser: str = Field(min_length=1)

    page_count: int = Field(ge=0)

    elements: list[Element] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_element_pages(self) -> "ParsedDocument":
        """
        Elementlerin sayfa numaralarının dokümanın
        toplam sayfa sayısını aşmadığını kontrol eder.
        """

        for element in self.elements:
            if element.page > self.page_count:
                raise ValueError(
                    f"Element sayfası ({element.page}), "
                    f"dokümanın toplam sayfa sayısından "
                    f"({self.page_count}) büyük olamaz."
                )

        return self

    def page_text(self, page: int) -> str:
        """Bir sayfadaki tüm elementlerin metnini sırayla birleştirir."""

        return "\n".join(element.text for element in self.elements if element.page == page)
