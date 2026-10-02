"""
LegalLens 2.0 - Task definitions base.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class TaskDefinition:
    """Base class for all LegalLens tasks."""
    id: str
    name: str
    description: str
    domain: str
    difficulty: int  # 1-5
    facts: str
    max_steps: int
    gold_standard: Dict[str, Any] = field(default_factory=dict)
    hints: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
