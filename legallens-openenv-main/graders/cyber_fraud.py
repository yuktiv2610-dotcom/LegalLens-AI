"""LegalLens 2.0 - Cyber Fraud Grader"""
from typing import Any, Dict
from environment.models import CaseState
from .base import BaseGrader


class CyberFraudGrader(BaseGrader):
    WEIGHTS = {
        "domain": 0.15,
        "issues": 0.20,
        "laws": 0.25,
        "jurisdiction": 0.10,
        "evidence": 0.15,
        "actions": 0.15,
    }

    def evaluate(self, state: CaseState, gold: Dict[str, Any]) -> Dict[str, Any]:
        breakdown = {
            "domain": self._score_domain(state, gold),
            "issues": self._score_issues(state, gold),
            "laws": self._score_laws(state, gold),
            "jurisdiction": self._score_jurisdiction(state, gold),
            "evidence": self._score_evidence(state, gold),
            "actions": self._score_actions(state, gold),
        }
        score = self._aggregate(breakdown, self.WEIGHTS)
        errors = []
        if not state.legal_domain:
            errors.append("No legal domain classified")
        if not state.identified_laws:
            errors.append("No laws identified")

        # Bonus: flagging cyber portal 1930
        action_text = " ".join(state.recommended_actions).lower()
        if "1930" in action_text or "cybercrime.gov.in" in action_text:
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
