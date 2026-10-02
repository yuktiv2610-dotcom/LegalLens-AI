"""LegalLens 2.0 - Graders package init."""
from .cyber_fraud import CyberFraudGrader
from .bail import BailGrader
from .consumer import ConsumerGrader
from .property import PropertyGrader

_ALL_GRADERS = {
    "cyber_fraud": CyberFraudGrader(),
    "bail": BailGrader(),
    "consumer": ConsumerGrader(),
    "property": PropertyGrader(),
}


def get_all_graders():
    return _ALL_GRADERS


def get_grader(task_id: str):
    if task_id not in _ALL_GRADERS:
        raise ValueError(f"No grader for task '{task_id}'")
    return _ALL_GRADERS[task_id]


__all__ = [
    "CyberFraudGrader", "BailGrader", "ConsumerGrader", "PropertyGrader",
    "get_all_graders", "get_grader",
]
