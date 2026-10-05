from enum import Enum


class AnswerType(str, Enum):
    FACTOID = "factoid"
    DESCRIPTIVE = "descriptive"
    NUMERIC = "numeric"


class ReasoningType(str, Enum):
    DIRECT = "direct"
    CALCULATION = "calculation"
    COMPARISON = "comparison"


class EvidenceRole(str, Enum):
    PRIMARY = "primary"
    SUPPORTING = "supporting"
    CALCULATION_INPUT = "calculation_input"


class EvalCaseStatus(str, Enum):
    GENERATED = "generated"
    VERIFIED = "verified"
    REJECTED = "rejected"
