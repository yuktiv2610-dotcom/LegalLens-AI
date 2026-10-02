"""
LegalLens 2.0 - Reward system.
Computes per-step and episode-level rewards based on action quality.
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from .models import ActionType, LegalAction, CaseState


# ---------------------------------------------------------------------------
# Base reward values
# ---------------------------------------------------------------------------

REWARD_TABLE: Dict[str, float] = {
    # Positive
    "correct_domain": 0.10,
    "correct_issue": 0.15,
    "relevant_law_verified": 0.20,
    "relevant_law_unverified": 0.05,
    "correct_jurisdiction": 0.10,
    "useful_evidence_requested": 0.10,
    "evidence_analyzed": 0.05,
    "appropriate_action": 0.10,
    "recognized_uncertainty": 0.10,  # For ASK_CLARIFICATION when facts are incomplete
    "finalize_complete": 0.15,
    "finalize_with_confidence": 0.05,
    # Negative
    "wrong_domain": -0.05,
    "irrelevant_law": -0.05,
    "contradictory_law": -0.10,
    "fabricated_citation": -0.20,
    "duplicate_action": -0.02,
    "irrelevant_evidence": -0.03,
    "premature_finalize": -0.15,
    "step_penalty": -0.01,  # Small per-step cost to encourage efficiency
}

MAX_EPISODE_REWARD = 1.0
MIN_EPISODE_REWARD = 0.0


def compute_step_reward(
    action: LegalAction,
    state_before: CaseState,
    state_after: CaseState,
    action_result: str,
    action_info: Dict[str, Any],
    task_gold: Dict[str, Any],
) -> float:
    """
    Compute the reward for a single action given the task's gold standard.

    task_gold contains:
        - correct_domain: str
        - relevant_issue_keywords: List[str]
        - relevant_law_ids: List[str]
        - correct_jurisdiction_keywords: List[str]
        - relevant_evidence_types: List[str]
        - correct_action_keywords: List[str]
        - facts_are_incomplete: bool (for uncertainty reward)
    """
    reward = 0.0
    action_type = action.action_type

    # Duplicate check (applies to all actions)
    if action_info.get("duplicate"):
        reward += REWARD_TABLE["duplicate_action"]
        return reward

    # --- CLASSIFY_DOMAIN ---
    if action_type == ActionType.CLASSIFY_DOMAIN:
        correct = task_gold.get("correct_domain", "")
        domain = (action.domain or "").lower()
        if correct and domain == correct.lower():
            reward += REWARD_TABLE["correct_domain"]
        elif correct:
            reward += REWARD_TABLE["wrong_domain"]

    # --- IDENTIFY_ISSUE ---
    elif action_type == ActionType.IDENTIFY_ISSUE:
        issue_kw = task_gold.get("relevant_issue_keywords", [])
        issue = (action.issue or "").lower()
        matched = any(kw.lower() in issue for kw in issue_kw)
        if matched:
            reward += REWARD_TABLE["correct_issue"]
        # no penalty for wrong issue, just no reward

    # --- IDENTIFY_LAW ---
    elif action_type == ActionType.IDENTIFY_LAW:
        relevant_ids = task_gold.get("relevant_law_ids", [])
        found_id = action_info.get("law_id") or ""
        is_unverified = action_info.get("unverified", False)
        found_in_kb = action_info.get("found", True)

        if is_unverified or not found_in_kb:
            # Fabricated or unverified citation penalty
            reward += REWARD_TABLE["fabricated_citation"]
        else:
            if found_id in relevant_ids:
                reward += REWARD_TABLE["relevant_law_verified"]
            else:
                reward += REWARD_TABLE["irrelevant_law"]

    # --- CHECK_JURISDICTION ---
    elif action_type == ActionType.CHECK_JURISDICTION:
        jkw = task_gold.get("correct_jurisdiction_keywords", [])
        jval = ((action.jurisdiction or "") + " " + (action.court or "")).lower()
        matched = any(kw.lower() in jval for kw in jkw)
        if matched:
            reward += REWARD_TABLE["correct_jurisdiction"]
        # no penalty for wrong jurisdiction identification

    # --- REQUEST_EVIDENCE ---
    elif action_type == ActionType.REQUEST_EVIDENCE:
        relevant_types = task_gold.get("relevant_evidence_types", [])
        ev_type = (action.evidence_type or "").upper()
        if ev_type in relevant_types:
            reward += REWARD_TABLE["useful_evidence_requested"]
        else:
            reward += REWARD_TABLE["irrelevant_evidence"]

    # --- ANALYZE_EVIDENCE ---
    elif action_type == ActionType.ANALYZE_EVIDENCE:
        if not action_info.get("error"):
            reward += REWARD_TABLE["evidence_analyzed"]

    # --- RECOMMEND_ACTION ---
    elif action_type == ActionType.RECOMMEND_ACTION:
        action_kw = task_gold.get("correct_action_keywords", [])
        rec = (action.action_recommendation or "").lower()
        matched = any(kw.lower() in rec for kw in action_kw)
        if matched:
            reward += REWARD_TABLE["appropriate_action"]

    # --- ASK_CLARIFICATION ---
    elif action_type == ActionType.ASK_CLARIFICATION:
        facts_incomplete = task_gold.get("facts_are_incomplete", False)
        if facts_incomplete:
            # Reward for recognizing uncertainty
            reward += REWARD_TABLE["recognized_uncertainty"]
        # If facts are complete and agent asks for clarification, small penalty
        elif not facts_incomplete and not state_after.missing_information:
            reward += -0.03

    # --- FINALIZE_ANALYSIS ---
    elif action_type == ActionType.FINALIZE_ANALYSIS:
        # Evaluate completeness
        has_domain = bool(state_after.legal_domain)
        has_issues = len(state_after.identified_issues) > 0
        has_laws = len(state_after.identified_laws) > 0
        has_evidence = len(state_after.evidence) > 0
        has_jurisdiction = bool(state_after.jurisdiction)
        has_actions = len(state_after.recommended_actions) > 0
        has_final = bool(state_after.final_analysis)

        completeness_score = sum([
            has_domain, has_issues, has_laws,
            has_evidence, has_jurisdiction, has_actions, has_final
        ]) / 7.0

        if completeness_score < 0.4:
            reward += REWARD_TABLE["premature_finalize"]
        else:
            reward += REWARD_TABLE["finalize_complete"] * completeness_score
            if state_after.confidence >= 0.6:
                reward += REWARD_TABLE["finalize_with_confidence"]

    # Small per-step cost
    reward += REWARD_TABLE["step_penalty"]

    return reward


def compute_final_score(
    state: CaseState,
    task_gold: Dict[str, Any],
    grader_score: float,
) -> float:
    """
    Compute final normalized episode score.
    Combines environment rewards + grader quality score.
    Result is clamped to [0.0, 1.0].
    """
    # Normalize cumulative reward
    # Expected max reward per episode ~ 1.0 (sum of all correct actions)
    EXPECTED_MAX_REWARD = 0.95
    env_score = max(0.0, min(1.0, state.cumulative_reward / EXPECTED_MAX_REWARD))

    # Weighted combination: 40% env reward + 60% grader evaluation
    final = 0.40 * env_score + 0.60 * grader_score

    return max(MIN_EPISODE_REWARD, min(MAX_EPISODE_REWARD, final))
