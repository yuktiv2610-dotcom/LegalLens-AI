"""LegalLens 2.0 - Property Dispute Grader"""
from typing import Any, Dict
from environment.models import CaseState
from .base import BaseGrader


class PropertyGrader(BaseGrader):
    WEIGHTS = {
        "domain": 0.10,
        "issues": 0.20,
        "laws": 0.25,
        "jurisdiction": 0.10,
        "evidence": 0.15,
        "actions": 0.15,
        "uncertainty": 0.05,
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
        if not state.identified_laws:
            errors.append("No property laws identified")

        # Bonus for injunction recommendation
        action_text = " ".join(state.recommended_actions).lower()
        if "injunction" in action_text:
            score = min(1.0, score + 0.05)

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
