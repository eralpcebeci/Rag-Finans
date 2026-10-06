from pathlib import Path

from rag.modules.evaluation.domain.models import EvalDataSet

PROJECT_ROOT = Path(__file__).resolve().parents[2]
GOLD_DATASET_PATH = PROJECT_ROOT / "data" / "evaluation" / "gold" / "pilot_gold_v1.json"


def test_pilot_gold_dataset_matches_domain_contract() -> None:
    dataset_json = GOLD_DATASET_PATH.read_text(encoding="utf-8")

    dataset = EvalDataSet.model_validate_json(dataset_json)

    assert len(dataset.cases) == 10
