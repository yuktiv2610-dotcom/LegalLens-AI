"""
LegalLens 2.0 - Pydantic models for actions, observations, and state.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, field_validator


# ---------------------------------------------------------------------------
# Action Space
# ---------------------------------------------------------------------------

class ActionType(str, Enum):
    CLASSIFY_DOMAIN = "CLASSIFY_DOMAIN"
    IDENTIFY_ISSUE = "IDENTIFY_ISSUE"
    IDENTIFY_LAW = "IDENTIFY_LAW"
    CHECK_JURISDICTION = "CHECK_JURISDICTION"
    REQUEST_EVIDENCE = "REQUEST_EVIDENCE"
    ANALYZE_EVIDENCE = "ANALYZE_EVIDENCE"
    RECOMMEND_ACTION = "RECOMMEND_ACTION"
    ASK_CLARIFICATION = "ASK_CLARIFICATION"
    FINALIZE_ANALYSIS = "FINALIZE_ANALYSIS"


class LegalAction(BaseModel):
    """A typed action in the LegalLens environment."""

    action_type: ActionType
    # Optional parameters depending on action type
    domain: Optional[str] = None              # CLASSIFY_DOMAIN
    issue: Optional[str] = None               # IDENTIFY_ISSUE
    law_reference: Optional[str] = None       # IDENTIFY_LAW
    law_id: Optional[str] = None              # IDENTIFY_LAW (preferred)
    jurisdiction: Optional[str] = None        # CHECK_JURISDICTION
    court: Optional[str] = None               # CHECK_JURISDICTION
    evidence_type: Optional[str] = None       # REQUEST_EVIDENCE
    evidence_id: Optional[str] = None         # ANALYZE_EVIDENCE
    analysis_notes: Optional[str] = None      # ANALYZE_EVIDENCE
    action_recommendation: Optional[str] = None  # RECOMMEND_ACTION
    question: Optional[str] = None            # ASK_CLARIFICATION
    missing_info: Optional[List[str]] = None  # ASK_CLARIFICATION
    final_analysis: Optional[str] = None      # FINALIZE_ANALYSIS
    confidence: Optional[float] = Field(None, ge=0.0, le=1.0)
    notes: Optional[str] = None

    class Config:
        extra = "allow"


# ---------------------------------------------------------------------------
# Evidence Model
# ---------------------------------------------------------------------------

class EvidenceItem(BaseModel):
    """A piece of evidence in a case."""

    id: str
    name: str
    evidence_type: str  # DOCUMENT, DIGITAL_RECORD, TRANSACTION, COMMUNICATION, WITNESS, PHOTOGRAPH, VIDEO, OFFICIAL_RECORD
    description: str
    status: str = "REQUIRED"  # REQUIRED, RECOMMENDED, MISSING, COLLECTED, VERIFIED
    relevance: str = ""
    collected: bool = False
    verified: bool = False
    metadata: Dict[str, Any] = Field(default_factory=dict)


# ---------------------------------------------------------------------------
# Law Reference Model
# ---------------------------------------------------------------------------

class LawReference(BaseModel):
    """A legal reference identified during analysis."""

    id: str
    name: str
    reference: str
    domain: str
    description: str
    relevance: str
    jurisdiction: str
    keywords: List[str] = Field(default_factory=list)
    verified: bool = True  # True = VERIFIED REFERENCE, False = REQUIRES VERIFICATION
    sections: List[str] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Case State
# ---------------------------------------------------------------------------

class CaseState(BaseModel):
    """Full mutable state of a legal case episode."""

    # Identity
    case_id: str
    task_id: str
    task_name: str
    episode_id: str

    # Case context
    facts: str
    legal_domain: Optional[str] = None
    jurisdiction: Optional[str] = None
    court_or_forum: Optional[str] = None

    # Identified elements
    identified_issues: List[str] = Field(default_factory=list)
    identified_laws: List[LawReference] = Field(default_factory=list)
    evidence: List[EvidenceItem] = Field(default_factory=list)
    recommended_actions: List[str] = Field(default_factory=list)
    missing_information: List[str] = Field(default_factory=list)
    clarification_questions: List[str] = Field(default_factory=list)

    # Reasoning chain
    action_history: List[Dict[str, Any]] = Field(default_factory=list)
    reasoning_nodes: List[Dict[str, Any]] = Field(default_factory=list)

    # Episode tracking
    step_count: int = 0
    max_steps: int = 20
    cumulative_reward: float = 0.0
    done: bool = False
    success: bool = False

    # Confidence
    confidence: float = 0.0  # 0.0 - 1.0

    # Timestamps
    started_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None

    # Final output
    final_analysis: Optional[str] = None
    final_score: Optional[float] = None


# ---------------------------------------------------------------------------
# Observation
# ---------------------------------------------------------------------------

class Observation(BaseModel):
    """What the agent sees after each step."""

    # Case facts (always visible)
    case_id: str
    task_id: str
    facts: str

    # Current known state
    legal_domain: Optional[str] = None
    jurisdiction: Optional[str] = None
    court_or_forum: Optional[str] = None
    identified_issues: List[str] = Field(default_factory=list)
    identified_laws: List[Dict[str, Any]] = Field(default_factory=list)
    evidence: List[Dict[str, Any]] = Field(default_factory=list)
    recommended_actions: List[str] = Field(default_factory=list)
    missing_information: List[str] = Field(default_factory=list)

    # Previous action feedback
    last_action: Optional[str] = None
    last_action_result: Optional[str] = None
    last_reward: float = 0.0
    last_error: Optional[str] = None

    # Episode status
    step_count: int = 0
    steps_remaining: int = 20
    cumulative_reward: float = 0.0
    done: bool = False
    confidence: float = 0.0

    # Hints
    available_actions: List[str] = Field(default_factory=list)
    suggested_next_action: Optional[str] = None


# ---------------------------------------------------------------------------
# Step Result
# ---------------------------------------------------------------------------

class StepResult(BaseModel):
    """Result of a single environment step."""

    observation: Observation
    reward: float
    done: bool
    info: Dict[str, Any] = Field(default_factory=dict)
    error: Optional[str] = None


# ---------------------------------------------------------------------------
# Episode Result
# ---------------------------------------------------------------------------

class EpisodeResult(BaseModel):
    """Final result of a complete episode."""

    task_id: str
    task_name: str
    case_id: str
    episode_id: str
    success: bool
    total_steps: int
    total_reward: float
    final_score: float  # 0.0 - 1.0 normalized
    rewards_per_step: List[float] = Field(default_factory=list)
    grader_breakdown: Dict[str, Any] = Field(default_factory=dict)
    errors: List[str] = Field(default_factory=list)
    feedback: str = ""
    final_analysis: Optional[str] = None
    duration_seconds: Optional[float] = None
