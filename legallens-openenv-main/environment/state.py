"""
LegalLens 2.0 - State management helpers.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any, Dict, List

from .models import CaseState, Observation, ActionType


def create_initial_state(task_id: str, task_name: str, case_id: str, facts: str, max_steps: int = 20) -> CaseState:
    """Create a fresh episode state for a task."""
    return CaseState(
        case_id=case_id,
        task_id=task_id,
        task_name=task_name,
        episode_id=str(uuid.uuid4()),
        facts=facts,
        max_steps=max_steps,
        started_at=datetime.utcnow(),
    )


def state_to_observation(
    state: CaseState,
    last_action: str = None,
    last_result: str = None,
    last_reward: float = 0.0,
    last_error: str = None,
) -> Observation:
    """Convert CaseState to an Observation (agent-facing view)."""
    steps_remaining = state.max_steps - state.step_count

    # Build law list (partial info — no gold answer)
    laws_visible = [
        {
            "id": law.id,
            "name": law.name,
            "reference": law.reference,
            "domain": law.domain,
            "description": law.description[:200],
            "verified": law.verified,
        }
        for law in state.identified_laws
    ]

    # Build evidence list
    evidence_visible = [
        {
            "id": ev.id,
            "name": ev.name,
            "evidence_type": ev.evidence_type,
            "status": ev.status,
            "description": ev.description[:200],
            "collected": ev.collected,
        }
        for ev in state.evidence
    ]

    # Available actions (all valid at any time)
    available = [a.value for a in ActionType]

    # Suggest next action based on state
    suggested = _suggest_next_action(state)

    return Observation(
        case_id=state.case_id,
        task_id=state.task_id,
        facts=state.facts,
        legal_domain=state.legal_domain,
        jurisdiction=state.jurisdiction,
        court_or_forum=state.court_or_forum,
        identified_issues=state.identified_issues,
        identified_laws=laws_visible,
        evidence=evidence_visible,
        recommended_actions=state.recommended_actions,
        missing_information=state.missing_information,
        last_action=last_action,
        last_action_result=last_result,
        last_reward=last_reward,
        last_error=last_error,
        step_count=state.step_count,
        steps_remaining=steps_remaining,
        cumulative_reward=state.cumulative_reward,
        done=state.done,
        confidence=state.confidence,
        available_actions=available,
        suggested_next_action=suggested,
    )


def _suggest_next_action(state: CaseState) -> str:
    """Simple heuristic to suggest the next logical action."""
    if not state.legal_domain:
        return ActionType.CLASSIFY_DOMAIN.value
    if not state.identified_issues:
        return ActionType.IDENTIFY_ISSUE.value
    if not state.identified_laws:
        return ActionType.IDENTIFY_LAW.value
    if not state.evidence:
        return ActionType.REQUEST_EVIDENCE.value
    if not state.jurisdiction:
        return ActionType.CHECK_JURISDICTION.value
    if not state.recommended_actions:
        return ActionType.RECOMMEND_ACTION.value
    if not state.final_analysis:
        return ActionType.FINALIZE_ANALYSIS.value
    return ActionType.FINALIZE_ANALYSIS.value


def record_action(state: CaseState, action_dict: Dict[str, Any], result: str, reward: float) -> None:
    """Record an action in the state's history."""
    state.action_history.append({
        "step": state.step_count,
        "action": action_dict,
        "result": result,
        "reward": round(reward, 4),
        "timestamp": datetime.utcnow().isoformat(),
    })


def is_terminal(state: CaseState) -> bool:
    """Check if the episode has reached a terminal state."""
    return state.done or state.step_count >= state.max_steps
