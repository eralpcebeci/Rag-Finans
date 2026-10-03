from typing import Self

from pydantic import BaseModel, Field, model_validator

from rag.modules.ingestion.domain.enums import ElementType

BBox = tuple[float, float, float, float]
# (x0, y0, x1, y1) -> sayfa üzerindeki dikdörtgen bölgenin koordinatları


class Element(BaseModel):
    """Bir sayfadaki tek bir normalize edilmiş içerik parçası."""

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

    source_file: str = Field(
        min_length=1,
        description="Kaynak dokümanın dosya adı.",
    )

    parser: str = Field(
        min_length=1,
        description="Dokümanı üreten ana parser.",
    )

    page_count: int = Field(
        ge=0,
        description="Dokümanın toplam sayfa sayısı.",
    )

    elements: list[Element] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_element_pages(self) -> Self:
        """
        Elementlerin sayfa numaralarının dokümanın toplam
        sayfa sayısını aşmadığını doğrular.
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
        """Belirtilen sayfadaki element metinlerini mevcut sırayla birleştirir."""

        return "\n".join(element.text for element in self.elements if element.page == page)
