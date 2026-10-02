#!/usr/bin/env python3
"""
LegalLens 2.0 - Root Inference Script (OpenEnv Standard)
Uses OpenAI client with configurable endpoint for LLM-driven agent.

Required environment variables:
  API_BASE_URL  - Base URL for OpenAI-compatible API (e.g., https://api-inference.huggingface.co/v1)
  MODEL_NAME    - Model to use (e.g., meta-llama/Llama-3.1-8B-Instruct)
  HF_TOKEN      - HuggingFace token (used as API key)

Output format (strict):
  [START] task=<name> env=legallens model=<model>
  [STEP] step=<n> action=<action> reward=<r> done=<true|false> error=<msg|null>
  [END] success=<true|false> steps=<n> score=<s> rewards=<r1,r2,...>
"""

from __future__ import annotations

import json
import os
import sys
import re
from typing import Any, Dict, List, Optional

# Ensure project root on path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------------------
# Configuration from environment
# ---------------------------------------------------------------------------

API_BASE_URL = os.environ.get("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.environ.get("MODEL_NAME", "gpt-4o-mini")
HF_TOKEN = os.environ.get("HF_TOKEN", os.environ.get("OPENAI_API_KEY", ""))
TASK_ID = os.environ.get("LEGALLENS_TASK", sys.argv[1] if len(sys.argv) > 1 else "cyber_fraud")
MAX_STEPS = int(os.environ.get("LEGALLENS_MAX_STEPS", "15"))

ENV_NAME = "legallens"

# ---------------------------------------------------------------------------
# System prompt for LLM agent
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """You are an expert Indian legal analyst AI agent operating in the LegalLens OpenEnv environment.

Your task is to analyze a legal case by taking structured actions one at a time.

AVAILABLE ACTIONS:
- CLASSIFY_DOMAIN: Classify the legal domain. Params: {"action_type": "CLASSIFY_DOMAIN", "domain": "<domain>"}
  Valid domains: cyber_law, criminal_law, consumer_law, property_law, civil_law
- IDENTIFY_ISSUE: Identify a specific legal issue. Params: {"action_type": "IDENTIFY_ISSUE", "issue": "<description>"}
- IDENTIFY_LAW: Identify a relevant law. Params: {"action_type": "IDENTIFY_LAW", "law_id": "<id>"} OR {"action_type": "IDENTIFY_LAW", "law_reference": "<reference>"}
- CHECK_JURISDICTION: Identify jurisdiction. Params: {"action_type": "CHECK_JURISDICTION", "jurisdiction": "<jurisdiction>", "court": "<court/forum>"}
- REQUEST_EVIDENCE: Request evidence. Params: {"action_type": "REQUEST_EVIDENCE", "evidence_type": "<type>", "notes": "<description>"}
  Valid types: DOCUMENT, DIGITAL_RECORD, TRANSACTION, COMMUNICATION, WITNESS, PHOTOGRAPH, OFFICIAL_RECORD
- ANALYZE_EVIDENCE: Analyze collected evidence. Params: {"action_type": "ANALYZE_EVIDENCE", "evidence_id": "<id>", "analysis_notes": "<notes>"}
- RECOMMEND_ACTION: Recommend a legal action. Params: {"action_type": "RECOMMEND_ACTION", "action_recommendation": "<recommendation>"}
- ASK_CLARIFICATION: Flag missing information. Params: {"action_type": "ASK_CLARIFICATION", "question": "<question>", "missing_info": ["<item1>", "<item2>"]}
- FINALIZE_ANALYSIS: Complete the analysis. Params: {"action_type": "FINALIZE_ANALYSIS", "final_analysis": "<full analysis>", "confidence": <0.0-1.0>}

RULES:
1. Always start with CLASSIFY_DOMAIN
2. You must identify at least 2 issues, 2 laws, and request evidence before finalizing
3. If facts are incomplete, use ASK_CLARIFICATION to flag missing information
4. Use only verified Indian law references
5. Your final analysis must be comprehensive and legally grounded
6. Never fabricate law citations — use only what you know is real Indian law

Respond with ONLY a JSON object for your action. No explanation, no markdown, just valid JSON."""


def _log(msg: str) -> None:
    """Log to stderr only."""
    print(msg, file=sys.stderr, flush=True)


def _emit(line: str) -> None:
    """Emit to stdout (structured output only)."""
    print(line, flush=True)


def build_user_message(observation: Dict[str, Any]) -> str:
    """Build a user message from the current observation."""
    parts = [
        f"CASE ID: {observation.get('case_id', 'N/A')}",
        f"TASK: {observation.get('task_id', 'N/A')}",
        "",
        "CASE FACTS:",
        observation.get("facts", "No facts available"),
        "",
        f"LEGAL DOMAIN: {observation.get('legal_domain') or 'Not yet classified'}",
        f"JURISDICTION: {observation.get('jurisdiction') or 'Not determined'}",
        f"COURT/FORUM: {observation.get('court_or_forum') or 'Not determined'}",
        "",
        "IDENTIFIED ISSUES:",
        "\n".join(f"  - {i}" for i in observation.get("identified_issues", [])) or "  (none yet)",
        "",
        "IDENTIFIED LAWS:",
        "\n".join(f"  - {l.get('reference', '')} ({l.get('name', '')})"
                  for l in observation.get("identified_laws", [])) or "  (none yet)",
        "",
        "EVIDENCE REQUESTED:",
        "\n".join(f"  - [{e.get('evidence_type', '')}] {e.get('name', '')}"
                  for e in observation.get("evidence", [])) or "  (none yet)",
        "",
        "RECOMMENDED ACTIONS:",
        "\n".join(f"  - {a}" for a in observation.get("recommended_actions", [])) or "  (none yet)",
        "",
        "MISSING INFORMATION:",
        "\n".join(f"  - {m}" for m in observation.get("missing_information", [])) or "  (none identified)",
        "",
        f"PREVIOUS ACTION: {observation.get('last_action') or 'N/A'}",
        f"PREVIOUS RESULT: {observation.get('last_action_result') or 'N/A'}",
        f"LAST REWARD: {observation.get('last_reward', 0.0)}",
        f"CUMULATIVE REWARD: {observation.get('cumulative_reward', 0.0)}",
        f"STEP: {observation.get('step_count', 0)} / {observation.get('step_count', 0) + observation.get('steps_remaining', 0)}",
        f"SUGGESTED NEXT ACTION: {observation.get('suggested_next_action') or 'Any'}",
        "",
        "Choose your next action as a JSON object:",
    ]
    return "\n".join(parts)


def parse_action_from_response(response_text: str) -> Optional[Dict[str, Any]]:
    """Extract JSON action from LLM response."""
    # Try direct JSON parse
    text = response_text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Try to find JSON block in response
    patterns = [
        r"```json\s*(.*?)\s*```",
        r"```\s*(.*?)\s*```",
        r"(\{.*?\})",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(1))
            except json.JSONDecodeError:
                continue

    _log(f"[WARN] Could not parse action from: {text[:200]}")
    return None


def run_inference(task_id: str = TASK_ID, max_steps: int = MAX_STEPS) -> None:
    """Main inference loop."""
    from openai import OpenAI
    from environment.env import LegalLensEnv

    client = OpenAI(
        base_url=API_BASE_URL,
        api_key=HF_TOKEN or "sk-no-key",
    )

    env = LegalLensEnv()

    _emit(f"[START] task={task_id} env={ENV_NAME} model={MODEL_NAME}")
    _log(f"[INFO] Starting inference: task={task_id} model={MODEL_NAME}")

    try:
        obs = env.reset(task_id=task_id)
    except ValueError as e:
        _emit(f"[END] success=false steps=0 score=0.0 rewards=")
        _log(f"[ERROR] Reset failed: {e}")
        sys.exit(1)

    conversation: List[Dict[str, str]] = []
    rewards: List[float] = []
    step = 0
    done = False

    while not done and step < max_steps:
        step += 1
        user_msg = build_user_message(obs.model_dump())
        conversation.append({"role": "user", "content": user_msg})

        # LLM call
        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role": "system", "content": SYSTEM_PROMPT}] + conversation,
                max_tokens=512,
                temperature=0.3,
            )
            assistant_text = response.choices[0].message.content or ""
        except Exception as e:
            _log(f"[ERROR] LLM call failed at step {step}: {e}")
            _emit(f"[STEP] step={step} action=null reward=0.0 done=false error={str(e)!r}")
            rewards.append(0.0)
            # Try to continue with a safe fallback
            if step >= 3:
                break
            continue

        conversation.append({"role": "assistant", "content": assistant_text})

        # Parse action
        action = parse_action_from_response(assistant_text)
        if action is None:
            _log(f"[WARN] Could not parse action at step {step}")
            _emit(f"[STEP] step={step} action=null reward=-0.02 done=false error=\"parse_error\"")
            rewards.append(-0.02)
            continue

        action_str = action.get("action_type", "unknown")

        # Execute
        try:
            result = env.step(action)
        except Exception as e:
            _log(f"[ERROR] Step execution failed: {e}")
            _emit(f"[STEP] step={step} action={action_str} reward=-0.05 done=false error={str(e)!r}")
            rewards.append(-0.05)
            continue

        reward = result.reward
        done = result.done
        obs = result.observation
        error_str = f'"{result.error}"' if result.error else "null"

        _emit(f"[STEP] step={step} action={action_str} reward={reward:.2f} done={'true' if done else 'false'} error={error_str}")
        _log(f"[DEBUG] Step {step}: {action_str} -> reward={reward:.4f}, done={done}")

        rewards.append(reward)

    # Compute final score
    ep = env.episode_result()
    final_score = ep.final_score if ep else 0.0
    success = ep.success if ep else (final_score >= 0.5)

    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    _emit(f"[END] success={'true' if success else 'false'} steps={step} score={final_score:.4f} rewards={rewards_str}")
    _log(f"[INFO] Episode complete: score={final_score:.4f}, steps={step}")


if __name__ == "__main__":
    run_inference()
