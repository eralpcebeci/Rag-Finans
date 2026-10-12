from pydantic import BaseModel, Field, field_validator

BBox = tuple[float, float, float, float]


class LayoutSpan(BaseModel):
    """PDF layout katmanından normalize edilmiş tek bir metin parçası."""

    text: str = Field(
        min_length=1,
        description="Span metni boş olmamalıdır.",
    )

    page: int = Field(
        ge=1,
        description="PDF sayfa numarası 1 veya daha büyük olmalıdır.",
    )

    bbox: BBox

    font_size: float = Field(
        gt=0,
        description="Font boyutu sıfırdan büyük olmalıdır.",
    )

    font_name: str = Field(
        min_length=1,
        description="Font adı boş olmamalıdır.",
    )

    is_bold: bool

    @field_validator("bbox")
    @classmethod
    def validate_bbox(cls, bbox: BBox) -> BBox:
        x0, y0, x1, y1 = bbox

        if x1 < x0:
            raise ValueError("bbox için x1, x0'dan küçük olamaz.")

        if y1 < y0:
            raise ValueError("bbox için y1, y0'dan küçük olamaz.")

        return bbox


class LayoutLine(BaseModel):
    """Aynı fiziksel satırdaki LayoutSpan nesnelerinin canonical temsili."""

    spans: list[LayoutSpan] = Field(
        min_length=1,
        description="Satırı oluşturan LayoutSpan nesneleri.",
    )

    @field_validator("spans")
    @classmethod
    def validate_spans_are_on_same_page(
        cls,
        spans: list[LayoutSpan],
    ) -> list[LayoutSpan]:
        pages = {span.page for span in spans}

        if len(pages) != 1:
            raise ValueError("LayoutLine içindeki tüm span'ler aynı sayfada olmalıdır.")

        return spans

    @property
    def text(self) -> str:
        return "".join(span.text for span in self.spans).strip()

    @property
    def page(self) -> int:
        return self.spans[0].page

    @property
    def bbox(self) -> BBox:
        return (
            min(span.bbox[0] for span in self.spans),
            min(span.bbox[1] for span in self.spans),
            max(span.bbox[2] for span in self.spans),
            max(span.bbox[3] for span in self.spans),
        )

    @property
    def max_font_size(self) -> float:
        return max(span.font_size for span in self.spans)

    @property
    def is_bold(self) -> bool:
        return any(span.is_bold for span in self.spans)
