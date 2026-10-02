"""
LegalLens 2.0 - Base grader class.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Dict, List

from environment.models import CaseState


class BaseGrader(ABC):
    """Abstract base class for all task graders."""

    @abstractmethod
    def evaluate(self, state: CaseState, gold: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate a completed episode.

        Returns:
            {
                "score": float (0.0 - 1.0),
                "breakdown": {component: score},
                "errors": [str],
                "feedback": str,
            }
        """
        pass

    def _score_domain(self, state: CaseState, gold: Dict) -> float:
        correct = gold.get("correct_domain", "")
        if not correct:
            return 0.5
        if state.legal_domain and state.legal_domain.lower() == correct.lower():
            return 1.0
        return 0.0

    def _score_issues(self, state: CaseState, gold: Dict) -> float:
        keywords = gold.get("relevant_issue_keywords", [])
        if not keywords or not state.identified_issues:
            return 0.0
        text = " ".join(state.identified_issues).lower()
        matched = sum(1 for kw in keywords if kw.lower() in text)
        return min(1.0, matched / max(1, len(keywords) * 0.4))

    def _score_laws(self, state: CaseState, gold: Dict) -> float:
        relevant_ids = set(gold.get("relevant_law_ids", []))
        if not relevant_ids:
            return 0.5
        identified_ids = {law.id for law in state.identified_laws if law.verified}
        unverified_count = sum(1 for law in state.identified_laws if not law.verified)
        if not identified_ids:
            return 0.0
        overlap = len(identified_ids & relevant_ids)
        base = min(1.0, overlap / max(1, len(relevant_ids) * 0.5))
        # Penalty for unverified/fabricated citations
        penalty = min(0.3, unverified_count * 0.1)
        return max(0.0, base - penalty)

    def _score_jurisdiction(self, state: CaseState, gold: Dict) -> float:
        jkw = gold.get("correct_jurisdiction_keywords", [])
        if not jkw:
            return 0.5
        jval = " ".join(filter(None, [state.jurisdiction, state.court_or_forum])).lower()
        if not jval:
            return 0.0
        matched = any(kw.lower() in jval for kw in jkw)
        return 1.0 if matched else 0.0

    def _score_evidence(self, state: CaseState, gold: Dict) -> float:
        relevant_types = gold.get("relevant_evidence_types", [])
        if not relevant_types or not state.evidence:
            return 0.0
        ev_types = {ev.evidence_type.upper() for ev in state.evidence}
        matched = len(ev_types & set(relevant_types))
        return min(1.0, matched / max(1, len(relevant_types) * 0.5))

    def _score_actions(self, state: CaseState, gold: Dict) -> float:
        action_kw = gold.get("correct_action_keywords", [])
        if not action_kw or not state.recommended_actions:
            return 0.0
        text = " ".join(state.recommended_actions).lower()
        matched = sum(1 for kw in action_kw if kw.lower() in text)
        return min(1.0, matched / max(1, len(action_kw) * 0.4))

    def _score_uncertainty(self, state: CaseState, gold: Dict) -> float:
        """Reward for correctly identifying missing information."""
        if not gold.get("facts_are_incomplete", False):
            return 1.0  # Not applicable — full marks
        required_missing = gold.get("required_missing_info", [])
        if not required_missing:
            return 0.5
        if not state.missing_information and not state.clarification_questions:
            return 0.0  # Failed to flag missing info
        identified_text = " ".join(
            state.missing_information + state.clarification_questions
        ).lower()
        matched = sum(1 for item in required_missing if item.lower() in identified_text)
        return min(1.0, matched / max(1, len(required_missing) * 0.5))

    def _score_completeness(self, state: CaseState, gold: Dict) -> float:
        """Score the overall completeness of the final analysis."""
        if not state.final_analysis:
            return 0.0
        has_domain = bool(state.legal_domain)
        has_laws = len(state.identified_laws) > 0
        has_evidence = len(state.evidence) > 0
        has_actions = len(state.recommended_actions) > 0
        has_analysis = bool(state.final_analysis) and len(state.final_analysis) > 50
        components = [has_domain, has_laws, has_evidence, has_actions, has_analysis]
        return sum(components) / len(components)

    def _aggregate(self, breakdown: Dict[str, float], weights: Dict[str, float]) -> float:
        total_weight = sum(weights.values())
        score = sum(breakdown.get(k, 0) * w for k, w in weights.items())
        return min(1.0, max(0.0, score / total_weight))
