"""
LegalLens 2.0 - Action validators and handlers.
Each action type is validated and dispatched here.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Any, Optional, Tuple

from .models import ActionType, LegalAction, CaseState, EvidenceItem, LawReference

if TYPE_CHECKING:
    pass


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

REQUIRED_PARAMS: Dict[ActionType, list] = {
    ActionType.CLASSIFY_DOMAIN: ["domain"],
    ActionType.IDENTIFY_ISSUE: ["issue"],
    ActionType.IDENTIFY_LAW: [],  # either law_id or law_reference
    ActionType.CHECK_JURISDICTION: [],  # either jurisdiction or court
    ActionType.REQUEST_EVIDENCE: ["evidence_type"],
    ActionType.ANALYZE_EVIDENCE: ["evidence_id"],
    ActionType.RECOMMEND_ACTION: ["action_recommendation"],
    ActionType.ASK_CLARIFICATION: ["question"],
    ActionType.FINALIZE_ANALYSIS: ["final_analysis"],
}

VALID_DOMAINS = [
    "cyber_law",
    "criminal_law",
    "consumer_law",
    "property_law",
    "civil_law",
    "constitutional_law",
    "family_law",
    "labor_law",
    "tax_law",
    "corporate_law",
    "environmental_law",
    "intellectual_property",
]

VALID_EVIDENCE_TYPES = [
    "DOCUMENT",
    "DIGITAL_RECORD",
    "TRANSACTION",
    "COMMUNICATION",
    "WITNESS",
    "PHOTOGRAPH",
    "VIDEO",
    "OFFICIAL_RECORD",
    "FINANCIAL_RECORD",
    "CONTRACT",
    "COMPLAINT",
    "MEDICAL_RECORD",
]


def validate_action(action: LegalAction, state: CaseState) -> Tuple[bool, Optional[str]]:
    """
    Validate an action against the current state.
    Returns (is_valid, error_message).
    """
    action_type = action.action_type

    # Check required parameters
    required = REQUIRED_PARAMS.get(action_type, [])
    for param in required:
        if getattr(action, param, None) is None:
            return False, f"Action {action_type.value} requires parameter '{param}'"

    # Episode-level checks
    if state.done:
        return False, "Episode is already complete. Call reset() to start a new episode."

    # Domain validation
    if action_type == ActionType.CLASSIFY_DOMAIN:
        if action.domain and action.domain.lower() not in VALID_DOMAINS:
            return False, (
                f"Unknown domain '{action.domain}'. Valid domains: {', '.join(VALID_DOMAINS)}"
            )

    # Law reference: must have at least one
    if action_type == ActionType.IDENTIFY_LAW:
        if not action.law_id and not action.law_reference:
            return False, "IDENTIFY_LAW requires either 'law_id' or 'law_reference'"

    # Jurisdiction: must have at least one
    if action_type == ActionType.CHECK_JURISDICTION:
        if not action.jurisdiction and not action.court:
            return False, "CHECK_JURISDICTION requires either 'jurisdiction' or 'court'"

    # Evidence type validation
    if action_type == ActionType.REQUEST_EVIDENCE:
        if action.evidence_type and action.evidence_type.upper() not in VALID_EVIDENCE_TYPES:
            return False, (
                f"Unknown evidence type '{action.evidence_type}'. "
                f"Valid types: {', '.join(VALID_EVIDENCE_TYPES)}"
            )

    # Finalize requires some prior work
    if action_type == ActionType.FINALIZE_ANALYSIS:
        if not state.legal_domain:
            return False, "Cannot finalize: no legal domain classified yet."
        if not state.identified_laws:
            return False, "Cannot finalize: no laws identified yet."

    return True, None


# ---------------------------------------------------------------------------
# Action Dispatch
# ---------------------------------------------------------------------------

def dispatch_action(
    action: LegalAction,
    state: CaseState,
    knowledge_base: Any,
) -> Tuple[CaseState, str, Dict[str, Any]]:
    """
    Apply an action to the state and return (new_state, result_message, info).
    Does NOT compute reward — that's the reward module's job.
    """
    action_type = action.action_type
    info: Dict[str, Any] = {"action_type": action_type.value}

    if action_type == ActionType.CLASSIFY_DOMAIN:
        return _classify_domain(action, state, knowledge_base, info)
    elif action_type == ActionType.IDENTIFY_ISSUE:
        return _identify_issue(action, state, knowledge_base, info)
    elif action_type == ActionType.IDENTIFY_LAW:
        return _identify_law(action, state, knowledge_base, info)
    elif action_type == ActionType.CHECK_JURISDICTION:
        return _check_jurisdiction(action, state, knowledge_base, info)
    elif action_type == ActionType.REQUEST_EVIDENCE:
        return _request_evidence(action, state, knowledge_base, info)
    elif action_type == ActionType.ANALYZE_EVIDENCE:
        return _analyze_evidence(action, state, knowledge_base, info)
    elif action_type == ActionType.RECOMMEND_ACTION:
        return _recommend_action(action, state, knowledge_base, info)
    elif action_type == ActionType.ASK_CLARIFICATION:
        return _ask_clarification(action, state, knowledge_base, info)
    elif action_type == ActionType.FINALIZE_ANALYSIS:
        return _finalize_analysis(action, state, knowledge_base, info)
    else:
        info["error"] = f"Unknown action type: {action_type}"
        return state, f"Unknown action: {action_type}", info


def _classify_domain(
    action: LegalAction, state: CaseState, kb: Any, info: Dict
) -> Tuple[CaseState, str, Dict]:
    domain = action.domain.lower().strip()
    state.legal_domain = domain
    info["domain"] = domain
    # Add reasoning node
    state.reasoning_nodes.append({
        "type": "domain",
        "value": domain,
        "step": state.step_count,
    })
    return state, f"Legal domain classified as: {domain}", info


def _identify_issue(
    action: LegalAction, state: CaseState, kb: Any, info: Dict
) -> Tuple[CaseState, str, Dict]:
    issue = action.issue.strip()
    if issue not in state.identified_issues:
        state.identified_issues.append(issue)
        state.reasoning_nodes.append({
            "type": "issue",
            "value": issue,
            "step": state.step_count,
        })
        info["issue"] = issue
        return state, f"Legal issue identified: {issue}", info
    else:
        info["duplicate"] = True
        return state, f"Issue already identified: {issue}", info


def _identify_law(
    action: LegalAction, state: CaseState, kb: Any, info: Dict
) -> Tuple[CaseState, str, Dict]:
    law_ref = None
    # Try to look up by ID first
    if action.law_id:
        law_ref = kb.get_law_by_id(action.law_id)
        info["law_id"] = action.law_id

    if law_ref is None and action.law_reference:
        # Look up by reference string
        law_ref = kb.find_law_by_reference(action.law_reference)
        info["law_reference"] = action.law_reference

    if law_ref:
        # Check for duplicate
        existing_ids = [l.id for l in state.identified_laws]
        if law_ref.id not in existing_ids:
            state.identified_laws.append(law_ref)
            state.reasoning_nodes.append({
                "type": "law",
                "value": law_ref.reference,
                "name": law_ref.name,
                "step": state.step_count,
            })
            info["found"] = True
            info["law_name"] = law_ref.name
            return state, f"Law identified: {law_ref.name} ({law_ref.reference})", info
        else:
            info["duplicate"] = True
            return state, f"Law already identified: {law_ref.name}", info
    else:
        # Not in KB — add as unverified reference
        ref_text = action.law_reference or action.law_id or "Unknown"
        unverified = LawReference(
            id=f"unverified_{len(state.identified_laws)}",
            name=ref_text,
            reference=ref_text,
            domain=state.legal_domain or "unknown",
            description="User-provided reference — requires verification",
            relevance="Unverified",
            jurisdiction="India",
            verified=False,
        )
        state.identified_laws.append(unverified)
        info["found"] = False
        info["unverified"] = True
        return state, f"Law reference noted (unverified): {ref_text}", info


def _check_jurisdiction(
    action: LegalAction, state: CaseState, kb: Any, info: Dict
) -> Tuple[CaseState, str, Dict]:
    jurisdiction = action.jurisdiction or action.court or ""
    state.jurisdiction = jurisdiction
    if action.court:
        state.court_or_forum = action.court
    info["jurisdiction"] = jurisdiction
    state.reasoning_nodes.append({
        "type": "jurisdiction",
        "value": jurisdiction,
        "court": action.court,
        "step": state.step_count,
    })
    return state, f"Jurisdiction determined: {jurisdiction}", info


def _request_evidence(
    action: LegalAction, state: CaseState, kb: Any, info: Dict
) -> Tuple[CaseState, str, Dict]:
    ev_type = action.evidence_type.upper() if action.evidence_type else "DOCUMENT"
    ev_id = f"ev_{len(state.evidence) + 1:03d}"
    desc = action.notes or f"{ev_type} evidence requested"
    evidence = EvidenceItem(
        id=ev_id,
        name=desc[:60],
        evidence_type=ev_type,
        description=desc,
        status="REQUIRED",
        relevance=action.notes or "",
        collected=False,
        verified=False,
    )
    # Avoid duplicates by type+description
    existing = [(e.evidence_type, e.description) for e in state.evidence]
    if (evidence.evidence_type, evidence.description) not in existing:
        state.evidence.append(evidence)
        state.reasoning_nodes.append({
            "type": "evidence",
            "value": ev_type,
            "description": desc,
            "step": state.step_count,
        })
        info["evidence_id"] = ev_id
        return state, f"Evidence requested: {ev_type} — {desc}", info
    else:
        info["duplicate"] = True
        return state, f"Evidence already requested: {ev_type}", info


def _analyze_evidence(
    action: LegalAction, state: CaseState, kb: Any, info: Dict
) -> Tuple[CaseState, str, Dict]:
    ev_id = action.evidence_id
    found = None
    for ev in state.evidence:
        if ev.id == ev_id:
            found = ev
            break

    if found:
        found.status = "COLLECTED"
        found.collected = True
        if action.analysis_notes:
            found.metadata["analysis"] = action.analysis_notes
        info["evidence_analyzed"] = ev_id
        return state, f"Evidence analyzed: {found.name} — status updated to COLLECTED", info
    else:
        info["error"] = f"Evidence ID '{ev_id}' not found"
        return state, f"Evidence '{ev_id}' not found. Request it first with REQUEST_EVIDENCE.", info


def _recommend_action(
    action: LegalAction, state: CaseState, kb: Any, info: Dict
) -> Tuple[CaseState, str, Dict]:
    rec = action.action_recommendation.strip()
    if rec not in state.recommended_actions:
        state.recommended_actions.append(rec)
        state.reasoning_nodes.append({
            "type": "action",
            "value": rec,
            "step": state.step_count,
        })
        info["recommendation"] = rec
        return state, f"Action recommended: {rec}", info
    else:
        info["duplicate"] = True
        return state, f"Recommendation already added: {rec}", info


def _ask_clarification(
    action: LegalAction, state: CaseState, kb: Any, info: Dict
) -> Tuple[CaseState, str, Dict]:
    question = action.question.strip()
    if question not in state.clarification_questions:
        state.clarification_questions.append(question)
        info["question"] = question

    if action.missing_info:
        for item in action.missing_info:
            if item not in state.missing_information:
                state.missing_information.append(item)
        info["missing_info"] = action.missing_info

    state.reasoning_nodes.append({
        "type": "clarification",
        "value": question,
        "missing": action.missing_info or [],
        "step": state.step_count,
    })
    return state, f"Clarification requested: {question}", info


def _finalize_analysis(
    action: LegalAction, state: CaseState, kb: Any, info: Dict
) -> Tuple[CaseState, str, Dict]:
    from datetime import datetime
    state.final_analysis = action.final_analysis
    if action.confidence is not None:
        state.confidence = action.confidence
    state.done = True
    state.completed_at = datetime.utcnow()
    info["finalized"] = True
    info["confidence"] = state.confidence
    return state, "Analysis finalized. Episode complete.", info
