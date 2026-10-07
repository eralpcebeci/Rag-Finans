import pytest
from pydantic import ValidationError

from rag.modules.evaluation.domain.enums import (
    AnswerType,
    EvidenceRole,
    ReasoningType,
)
from rag.modules.evaluation.domain.models import (
    CapabilityTag,
    EvalCase,
    EvalDataSet,
    EvidenceItem,
)


def test_direct_eval_case_accepts_primary_evidence() -> None:
    evidence = EvidenceItem(
        source_file="akbank_2025_faaliyet.pdf",
        page=100,
        text="Örnek kaynak metin.",
        role=EvidenceRole.PRIMARY,
    )

    eval_case = EvalCase(
        id="akbank-2025-001",
        question="Örnek soru nedir?",
        reference_answer="Örnek cevap.",
        answer_type=AnswerType.FACTOID,
        reasoning_type=ReasoningType.DIRECT,
        category="test",
        evidence=[evidence],
    )

    assert eval_case.reasoning_type == ReasoningType.DIRECT
    assert eval_case.evidence[0].role == EvidenceRole.PRIMARY


def test_direct_eval_case_rejects_without_primary_evidence() -> None:
    evidence = EvidenceItem(
        source_file="akbank_2025_faaliyet.pdf",
        page=100,
        text="Destekleyici kaynak metin.",
        role=EvidenceRole.SUPPORTING,
    )

    with pytest.raises(
        ValidationError,
        match="DIRECT EvalCase en az bir PRIMARY evidence içermelidir",
    ):
        EvalCase(
            id="akbank-2025-002",
            question="Örnek soru nedir?",
            reference_answer="Örnek cevap.",
            answer_type=AnswerType.FACTOID,
            reasoning_type=ReasoningType.DIRECT,
            category="test",
            evidence=[evidence],
        )


def test_calculation_eval_case_accepts_calculation_input_evidence() -> None:
    evidence = EvidenceItem(
        source_file="akbank_2025_faaliyet.pdf",
        page=195,
        text="Geçmeli kaynak metin.",
        role=EvidenceRole.CALCULATION_INPUT,
    )

    eval_case = EvalCase(
        id="akbank-2025-003",
        question="2024'e göre 2025 net kâr yüzde kaç arttı?",
        reference_answer="%20 arttı.",
        answer_type=AnswerType.NUMERIC,
        reasoning_type=ReasoningType.CALCULATION,
        category="profitability",
        evidence=[evidence],
    )

    assert eval_case.reasoning_type == ReasoningType.CALCULATION
    assert eval_case.evidence[0].role == EvidenceRole.CALCULATION_INPUT


def test_calculation_eval_case_rejects_without_calculation_input_evidence() -> None:
    evidence = EvidenceItem(
        source_file="akbank_2025_faaliyet.pdf",
        page=243,
        text="Hesaplama sorusunu destekleyen kaynak.",
        role=EvidenceRole.PRIMARY,
    )

    with pytest.raises(
        ValidationError,
        match=("CALCULATION EvalCase en az bir " "CALCULATION_INPUT evidence içermelidir"),
    ):
        EvalCase(
            id="akbank-2025-004",
            question="2025 dönem kârı yüzde kaç arttı?",
            reference_answer="%5",
            answer_type=AnswerType.NUMERIC,
            reasoning_type=ReasoningType.CALCULATION,
            category="test",
            evidence=[evidence],
        )


def test_eval_dataset_rejects_duplicate_case_ids() -> None:
    evidence_1 = EvidenceItem(
        source_file="akbank_2025_faaliyet.pdf",
        page=100,
        text="Birinci Kanıt",
        role=EvidenceRole.PRIMARY,
    )

    evidence_2 = EvidenceItem(
        source_file="akbank_2025_faaliyet.pdf",
        page=250,
        text="İkinci Kanıt",
        role=EvidenceRole.PRIMARY,
    )

    case_1 = EvalCase(
        id="akbank-2025-001",
        question="Birinci soru?",
        reference_answer="Birinci cevap.",
        answer_type=AnswerType.FACTOID,
        reasoning_type=ReasoningType.DIRECT,
        category="test",
        evidence=[evidence_1],
    )

    case_2 = EvalCase(
        id="akbank-2025-001",  # Bilerek aynı ID
        question="İkinci soru?",
        reference_answer="İkinci cevap.",
        answer_type=AnswerType.FACTOID,
        reasoning_type=ReasoningType.DIRECT,
        category="test",
        evidence=[evidence_2],
    )

    with pytest.raises(
        ValidationError,
        match="EvalDataset içindeki EvalCase id değerleri benzersiz olmalıdır",
    ):
        EvalDataSet(cases=[case_1, case_2])


def test_eval_dataset_accepts_unique_case_ids() -> None:
    evidence_1 = EvidenceItem(
        source_file="akbank_2025_faaliyet.pdf",
        page=110,
        text="Birinci Kanıt",
        role=EvidenceRole.PRIMARY,
    )

    evidence_2 = EvidenceItem(
        source_file="akbank_2025_faaliyet.pdf",
        page=703,
        text="İkinci Kanıt",
        role=EvidenceRole.PRIMARY,
    )

    case_1 = EvalCase(
        id="akbank-2025-001",
        question="Birinci soru?",
        reference_answer="Birinci cevap.",
        answer_type=AnswerType.FACTOID,
        reasoning_type=ReasoningType.DIRECT,
        category="test",
        evidence=[evidence_1],
    )

    case_2 = EvalCase(
        id="akbank-2025-002",
        question="İkinci soru?",
        reference_answer="İkinci cevap.",
        answer_type=AnswerType.FACTOID,
        reasoning_type=ReasoningType.DIRECT,
        category="test",
        evidence=[evidence_2],
    )

    dataset = EvalDataSet(cases=[case_1, case_2])

    assert len(dataset.cases) == 2
    assert dataset.cases[0].id == "akbank-2025-001"
    assert dataset.cases[1].id == "akbank-2025-002"


def test_eval_dataset_rejects_empty_cases() -> None:
    with pytest.raises(ValidationError):
        EvalDataSet(cases=[])


def test_eval_case_defaults_to_empty_tags() -> None:
    evidence = EvidenceItem(
        source_file="akbank_2025_faaliyet.pdf",
        page=100,
        text="örnek kaynak metin",
        role=EvidenceRole.PRIMARY,
    )

    eval_case = EvalCase(
        id="akbank-2025-tag-001",
        question="Örnek Soru",
        reference_answer="Örnek Cevap",
        answer_type=AnswerType.FACTOID,
        reasoning_type=ReasoningType.DIRECT,
        category="test",
        evidence=[evidence],
    )
    assert eval_case.tags == []


def test_eval_case_accepts_valid_capability_tag() -> None:
    evidence = EvidenceItem(
        source_file="akbank_2025_faaliyet.pdf",
        page=100,
        text="örnek kaynak metin",
        role=EvidenceRole.PRIMARY,
    )

    eval_case = EvalCase(
        id="akbank-2025-tags-002",
        question="Tablodaki Değer Nedir",
        reference_answer="5,46",
        answer_type=AnswerType.NUMERIC,
        reasoning_type=ReasoningType.DIRECT,
        category="test",
        tags=[CapabilityTag.TABLE_HEAVY],
        evidence=[evidence],
    )

    assert eval_case.tags == [CapabilityTag.TABLE_HEAVY]


def test_eval_case_rejects_unkown_capability_tag() -> None:
    evidence = EvidenceItem(
        source_file="akbank_2025_faaliyet.pdf",
        page=130,
        text="Örnek Kaynak Metin",
        role=EvidenceRole.PRIMARY,
    )

    with pytest.raises(ValidationError):
        EvalCase(
            id="akbank-2025-tags-003",
            question="örnek soru",
            reference_answer="örnek cevap",
            answer_type=AnswerType.FACTOID,
            reasoning_type=ReasoningType.DIRECT,
            category="test",
            tags=["table_heawy"],
            evidence=[evidence],
        )
