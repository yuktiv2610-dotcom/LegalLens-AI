"""
LegalLens 2.0 - OpenEnv AI Legal Reasoning Environment
Core environment package.
"""

from .env import LegalLensEnv
from .models import (
    ActionType,
    LegalAction,
    Observation,
    CaseState,
    StepResult,
    EpisodeResult,
)

__all__ = [
    "LegalLensEnv",
    "ActionType",
    "LegalAction",
    "Observation",
    "CaseState",
    "StepResult",
    "EpisodeResult",
]
