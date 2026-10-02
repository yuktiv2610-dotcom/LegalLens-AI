"""LegalLens 2.0 - Bail Grader (rewards uncertainty recognition)"""
from typing import Any, Dict
from environment.models import CaseState
from .base import BaseGrader


class BailGrader(BaseGrader):
    WEIGHTS = {
        "domain": 0.10,
        "issues": 0.15,
        "laws": 0.20,
        "jurisdiction": 0.10,
        "evidence": 0.10,
        "actions": 0.15,
        "uncertainty": 0.20,  # Key weight for bail task
    }

    def evaluate(self, state: CaseState, gold: Dict[str, Any]) -> Dict[str, Any]:
        breakdown = {
            "domain": self._score_domain(state, gold),
            "issues": self._score_issues(state, gold),
            "laws": self._score_laws(state, gold),
            "jurisdiction": self._score_jurisdiction(state, gold),
            "evidence": self._score_evidence(state, gold),
            "actions": self._score_actions(state, gold),
            "uncertainty": self._score_uncertainty(state, gold),
        }
        score = self._aggregate(breakdown, self.WEIGHTS)
        errors = []
        if not state.missing_information and not state.clarification_questions:
            errors.append("Agent did not identify missing critical information (charges, offence type)")

        feedback_parts = []
        for k, v in breakdown.items():
            pct = int(v * 100)
            feedback_parts.append(f"{k.upper()}: {pct}%")

        return {
            "score": round(score, 4),
            "breakdown": {k: round(v, 4) for k, v in breakdown.items()},
            "errors": errors,
            "feedback": " | ".join(feedback_parts),
        }
