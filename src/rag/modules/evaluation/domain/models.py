from typing import Self

from pydantic import BaseModel, Field, model_validator

from rag.modules.evaluation.domain.enums import (
    AnswerType,
    EvalCaseStatus,
    EvidenceRole,
    ReasoningType,
)

BBox = tuple[float, float, float, float]


class EvidenceItem(BaseModel):
    """Bir referans cevabı destekleyen kaynak kanıt."""

    source_file: str = Field(
        min_length=1,
        description="Kanıtın alındığı kaynak doküman.",
    )

    page: int = Field(
        ge=1,
        description="Kanıtın bulunduğu PDF sayfası.",
    )

    text: str = Field(
        min_length=1,
        description="Cevabı destekleyen kaynak metin.",
    )

    role: EvidenceRole = EvidenceRole.PRIMARY

    bbox: BBox | None = None


class EvalCase(BaseModel):
    """RAG sistemini değerlendirmek için tek bir referans senaryosu."""

    id: str = Field(
        min_length=1,
        description="Eval case için kararlı benzersiz kimlik.",
    )

    question: str = Field(
        min_length=1,
        description="Sisteme sorulacak soru.",
    )

    reference_answer: str = Field(
        min_length=1,
        description="Beklenen referans cevap.",
    )

    answer_type: AnswerType

    reasoning_type: ReasoningType

    category: str = Field(
        min_length=1,
        description="Sorunun finansal veya dokümansal kategorisi.",
    )

    evidence: list[EvidenceItem] = Field(
        min_length=1,
        description="Referans cevabı destekleyen kanıtlar.",
    )

    status: EvalCaseStatus = EvalCaseStatus.GENERATED

    @model_validator(mode="after")
    def validate_evidence_roles(self) -> Self:
        if self.reasoning_type == ReasoningType.DIRECT:
            if not any(item.role == EvidenceRole.PRIMARY for item in self.evidence):
                raise ValueError("DIRECT EvalCase en az bir PRIMARY evidence içermelidir.")

        if self.reasoning_type == ReasoningType.CALCULATION:
            if not any(item.role == EvidenceRole.CALCULATION_INPUT for item in self.evidence):
                raise ValueError(
                    "CALCULATION EvalCase en az bir " "CALCULATION_INPUT evidence içermelidir."
                )

        return self


class EvalDataSet(BaseModel):
    """Birden fazla EvalCase içeren değerlendirme veri seti."""

    cases: list[EvalCase] = Field(
        min_length=1,
        description="Değerlendirme veri setindeki senaryolar.",
    )

    @model_validator(mode="after")
    def validate_unique_case_ids(self) -> Self:
        case_ids = [case.id for case in self.cases]

        if len(case_ids) != len(set(case_ids)):
            raise ValueError("EvalDataset içindeki EvalCase id değerleri benzersiz olmalıdır")
        return self
