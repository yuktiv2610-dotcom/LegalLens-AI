"""
LegalLens 2.0 - Core OpenEnv environment.
Exposes reset(), step(), state() interface.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from .actions import dispatch_action, validate_action
from .models import (
    ActionType,
    CaseState,
    EpisodeResult,
    LegalAction,
    Observation,
    StepResult,
)
from .rewards import compute_final_score, compute_step_reward
from .state import (
    create_initial_state,
    is_terminal,
    record_action,
    state_to_observation,
)


class LegalLensEnv:
    """
    OpenEnv-compatible environment for Indian legal reasoning.

    Usage:
        env = LegalLensEnv()
        obs = env.reset(task_id="cyber_fraud")
        result = env.step({"action_type": "CLASSIFY_DOMAIN", "domain": "cyber_law"})
        state = env.state()
    """

    def __init__(self):
        self._state: Optional[CaseState] = None
        self._task_gold: Dict[str, Any] = {}
        self._rewards_log: List[float] = []
        self._knowledge_base = None
        self._tasks: Dict[str, Any] = {}
        self._graders: Dict[str, Any] = {}
        self._initialized = False

    # ------------------------------------------------------------------
    # Initialization
    # ------------------------------------------------------------------

    def _ensure_initialized(self):
        if not self._initialized:
            self._load_components()
            self._initialized = True

    def _load_components(self):
        """Lazy-load knowledge base, tasks, and graders."""
        from legal.knowledge_base import LegalKnowledgeBase
        from tasks import get_all_tasks
        from graders import get_all_graders

        self._knowledge_base = LegalKnowledgeBase()
        self._tasks = get_all_tasks()
        self._graders = get_all_graders()

    # ------------------------------------------------------------------
    # OpenEnv Interface
    # ------------------------------------------------------------------

    def reset(self, task_id: str = "cyber_fraud", **kwargs) -> Observation:
        """
        Reset the environment for a new episode.

        Args:
            task_id: One of 'cyber_fraud', 'bail', 'consumer', 'property'

        Returns:
            Initial observation.
        """
        self._ensure_initialized()

        if task_id not in self._tasks:
            available = list(self._tasks.keys())
            raise ValueError(f"Unknown task '{task_id}'. Available: {available}")

        task = self._tasks[task_id]
        case_id = f"CASE-{task_id.upper()[:3]}-{uuid.uuid4().hex[:6].upper()}"

        self._state = create_initial_state(
            task_id=task_id,
            task_name=task.name,
            case_id=case_id,
            facts=task.facts,
            max_steps=task.max_steps,
        )
        self._task_gold = task.gold_standard
        self._rewards_log = []

        return state_to_observation(
            self._state,
            last_result="Environment reset. New case presented.",
        )

    def step(self, action: Dict[str, Any]) -> StepResult:
        """
        Execute one action in the environment.

        Args:
            action: Dict with 'action_type' and optional parameters.

        Returns:
            StepResult with observation, reward, done flag, and info.
        """
        self._ensure_initialized()

        if self._state is None:
            raise RuntimeError("Environment not reset. Call reset() first.")

        # Parse action
        try:
            legal_action = LegalAction(**action)
        except Exception as e:
            # Return controlled error instead of crash
            obs = state_to_observation(self._state, last_error=str(e))
            return StepResult(
                observation=obs,
                reward=-0.05,
                done=False,
                info={"parse_error": str(e)},
                error=str(e),
            )

        # Check terminal
        if is_terminal(self._state):
            obs = state_to_observation(self._state, last_result="Episode already complete.")
            return StepResult(observation=obs, reward=0.0, done=True, info={"terminal": True})

        # Validate action
        is_valid, validation_error = validate_action(legal_action, self._state)
        if not is_valid:
            obs = state_to_observation(
                self._state,
                last_action=legal_action.action_type.value,
                last_error=validation_error,
                last_reward=-0.02,
            )
            self._state.cumulative_reward += -0.02
            return StepResult(
                observation=obs,
                reward=-0.02,
                done=False,
                info={"validation_error": validation_error},
                error=validation_error,
            )

        # Dispatch action
        state_before = self._state.model_copy(deep=True)
        self._state, result_msg, action_info = dispatch_action(
            legal_action, self._state, self._knowledge_base
        )

        # Increment step
        self._state.step_count += 1

        # Compute reward
        reward = compute_step_reward(
            action=legal_action,
            state_before=state_before,
            state_after=self._state,
            action_result=result_msg,
            action_info=action_info,
            task_gold=self._task_gold,
        )
        self._state.cumulative_reward += reward
        self._rewards_log.append(round(reward, 4))

        # Record in history
        record_action(self._state, action, result_msg, reward)

        # Check terminal again
        done = is_terminal(self._state)
        if done and self._state.final_analysis:
            self._state.success = True

        # Force terminal if max steps reached
        if self._state.step_count >= self._state.max_steps and not self._state.done:
            self._state.done = True
            done = True

        obs = state_to_observation(
            self._state,
            last_action=legal_action.action_type.value,
            last_result=result_msg,
            last_reward=reward,
        )

        return StepResult(
            observation=obs,
            reward=round(reward, 4),
            done=done,
            info=action_info,
        )

    def state(self) -> Dict[str, Any]:
        """Return full internal state as a dict."""
        self._ensure_initialized()
        if self._state is None:
            return {"status": "not_reset", "message": "Call reset() first."}
        return self._state.model_dump()

    def episode_result(self) -> Optional[EpisodeResult]:
        """Compute and return full episode result with grader evaluation."""
        self._ensure_initialized()
        if self._state is None:
            return None

        task_id = self._state.task_id
        grader = self._graders.get(task_id)
        grader_result = {"score": 0.5, "breakdown": {}, "errors": [], "feedback": ""}

        if grader:
            try:
                grader_result = grader.evaluate(self._state, self._task_gold)
            except Exception as e:
                grader_result["errors"].append(str(e))

        final_score = compute_final_score(
            self._state, self._task_gold, grader_result.get("score", 0.5)
        )
        self._state.final_score = final_score

        started = self._state.started_at
        completed = self._state.completed_at or datetime.utcnow()
        duration = (completed - started).total_seconds()

        return EpisodeResult(
            task_id=self._state.task_id,
            task_name=self._state.task_name,
            case_id=self._state.case_id,
            episode_id=self._state.episode_id,
            success=self._state.success,
            total_steps=self._state.step_count,
            total_reward=round(self._state.cumulative_reward, 4),
            final_score=round(final_score, 4),
            rewards_per_step=self._rewards_log,
            grader_breakdown=grader_result.get("breakdown", {}),
            errors=grader_result.get("errors", []),
            feedback=grader_result.get("feedback", ""),
            final_analysis=self._state.final_analysis,
            duration_seconds=round(duration, 2),
        )

    # ------------------------------------------------------------------
    # Convenience
    # ------------------------------------------------------------------

    @property
    def task_ids(self) -> List[str]:
        self._ensure_initialized()
        return list(self._tasks.keys())

    @property
    def is_reset(self) -> bool:
        return self._state is not None
