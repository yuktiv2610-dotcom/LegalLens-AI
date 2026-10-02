"""
LegalLens 2.0 - FastAPI Server
Exposes OpenEnv interface + REST API for frontend.
"""

from __future__ import annotations

import sys
import os
import uuid
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from environment.env import LegalLensEnv
from environment.models import LegalAction

app = FastAPI(
    title="LegalLens 2.0",
    description="OpenEnv AI Legal Reasoning Environment for Indian Law",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Session storage (in-memory, keyed by session_id)
_sessions: Dict[str, LegalLensEnv] = {}

DISCLAIMER = (
    "LegalLens is an AI-assisted informational tool. "
    "It does not provide professional legal advice. "
    "Verify applicable law and consult a qualified professional for real-world legal decisions."
)


# ---------------------------------------------------------------------------
# Request/Response Models
# ---------------------------------------------------------------------------

class ResetRequest(BaseModel):
    task_id: str = "cyber_fraud"
    session_id: Optional[str] = None


class StepRequest(BaseModel):
    session_id: str
    action: Dict[str, Any]


class AgentRunRequest(BaseModel):
    task_id: str = "cyber_fraud"
    max_steps: int = 15


class WhatIfRequest(BaseModel):
    session_id: str
    modified_fact: str
    task_id: Optional[str] = None


# ---------------------------------------------------------------------------
# Health
# ---------------------------------------------------------------------------

@app.get("/health")
async def health():
    """Health check endpoint. Returns 200 when system is operational."""
    return {
        "status": "healthy",
        "version": "2.0.0",
        "disclaimer": DISCLAIMER,
    }


# ---------------------------------------------------------------------------
# OpenEnv Interface
# ---------------------------------------------------------------------------

@app.post("/reset")
async def openenv_reset(req: ResetRequest):
    """OpenEnv reset endpoint. Returns initial observation."""
    session_id = req.session_id or str(uuid.uuid4())
    env = LegalLensEnv()
    try:
        obs = env.reset(task_id=req.task_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    _sessions[session_id] = env
    return {
        "session_id": session_id,
        "observation": obs.model_dump(),
        "task_id": req.task_id,
        "disclaimer": DISCLAIMER,
    }


@app.post("/step")
async def openenv_step(req: StepRequest):
    """OpenEnv step endpoint. Executes an action and returns observation+reward."""
    env = _sessions.get(req.session_id)
    if env is None:
        raise HTTPException(status_code=404, detail=f"Session '{req.session_id}' not found. Call /reset first.")
    result = env.step(req.action)
    response = {
        "observation": result.observation.model_dump(),
        "reward": result.reward,
        "done": result.done,
        "info": result.info,
    }
    if result.error:
        response["error"] = result.error
    if result.done:
        ep = env.episode_result()
        if ep:
            response["episode_result"] = ep.model_dump()
    return response


@app.get("/state")
async def openenv_state(session_id: str):
    """OpenEnv state endpoint. Returns full internal state."""
    env = _sessions.get(session_id)
    if env is None:
        raise HTTPException(status_code=404, detail=f"Session '{session_id}' not found.")
    return env.state()


# ---------------------------------------------------------------------------
# Tasks API
# ---------------------------------------------------------------------------

@app.get("/api/tasks")
async def get_tasks():
    """List all available tasks."""
    from tasks import get_all_tasks
    tasks = get_all_tasks()
    return {
        "tasks": [
            {
                "id": t.id,
                "name": t.name,
                "description": t.description,
                "domain": t.domain,
                "difficulty": t.difficulty,
                "max_steps": t.max_steps,
                "tags": t.tags,
            }
            for t in tasks.values()
        ]
    }


@app.get("/api/tasks/{task_id}")
async def get_task(task_id: str):
    """Get details for a specific task (without gold standard)."""
    from tasks import get_all_tasks
    tasks = get_all_tasks()
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail=f"Task '{task_id}' not found.")
    t = tasks[task_id]
    return {
        "id": t.id,
        "name": t.name,
        "description": t.description,
        "domain": t.domain,
        "difficulty": t.difficulty,
        "max_steps": t.max_steps,
        "facts": t.facts,
        "hints": t.hints,
        "tags": t.tags,
    }


# ---------------------------------------------------------------------------
# Case API (frontend-facing convenience wrappers)
# ---------------------------------------------------------------------------

@app.post("/api/case/reset")
async def case_reset(req: ResetRequest):
    """Alias for /reset — used by frontend."""
    return await openenv_reset(req)


@app.post("/api/case/step")
async def case_step(req: StepRequest):
    """Alias for /step — used by frontend."""
    return await openenv_step(req)


@app.get("/api/case/state")
async def case_state(session_id: str):
    """Alias for /state — used by frontend."""
    return await openenv_state(session_id)


@app.get("/api/case/result")
async def case_result(session_id: str):
    """Get episode result for a completed session."""
    env = _sessions.get(session_id)
    if env is None:
        raise HTTPException(status_code=404, detail=f"Session '{session_id}' not found.")
    ep = env.episode_result()
    if ep is None:
        raise HTTPException(status_code=400, detail="Episode not yet complete.")
    return ep.model_dump()


# ---------------------------------------------------------------------------
# Laws API
# ---------------------------------------------------------------------------

@app.get("/api/laws")
async def get_laws(domain: Optional[str] = None, query: Optional[str] = None):
    """Get laws from the knowledge base, optionally filtered."""
    from legal.knowledge_base import LegalKnowledgeBase
    kb = LegalKnowledgeBase()
    if query:
        laws = kb.search_laws(query)
    elif domain:
        laws = kb.get_laws_by_domain(domain)
    else:
        laws = kb.get_all_laws()
    return {
        "laws": [law.model_dump() for law in laws],
        "count": len(laws),
    }


@app.get("/api/laws/{law_id}")
async def get_law(law_id: str):
    """Get a specific law by ID."""
    from legal.knowledge_base import LegalKnowledgeBase
    kb = LegalKnowledgeBase()
    law = kb.get_law_by_id(law_id)
    if law is None:
        raise HTTPException(status_code=404, detail=f"Law '{law_id}' not found.")
    return law.model_dump()


# ---------------------------------------------------------------------------
# Agent Lab — run baseline agent in-process for demo
# ---------------------------------------------------------------------------

@app.post("/api/agent/run")
async def agent_run(req: AgentRunRequest):
    """
    Run the baseline heuristic agent on a task and stream results.
    Returns a list of steps with rewards.
    """
    from baseline_agent import BaselineAgent
    agent = BaselineAgent()
    try:
        result = agent.run(task_id=req.task_id, max_steps=req.max_steps)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---------------------------------------------------------------------------
# What-If Mode
# ---------------------------------------------------------------------------

@app.post("/api/case/whatif")
async def case_whatif(req: WhatIfRequest):
    """
    Create a new episode with one modified fact.
    Returns new session_id with the alternative analysis.
    """
    original_env = _sessions.get(req.session_id)
    if original_env is None:
        raise HTTPException(status_code=404, detail=f"Session '{req.session_id}' not found.")

    original_state = original_env.state()
    task_id = req.task_id or original_state.get("task_id", "cyber_fraud")

    from tasks import get_task
    task = get_task(task_id)

    # Create modified facts
    modified_facts = task.facts + f"\n\n[WHAT-IF MODIFICATION]\n{req.modified_fact}"

    # Start new session with modified facts
    new_session_id = f"whatif-{uuid.uuid4().hex[:8]}"
    new_env = LegalLensEnv()
    new_env._ensure_initialized()
    from environment.state import create_initial_state
    from environment.models import CaseState
    import uuid as _uuid

    case_id = f"WHATIF-{task_id.upper()[:3]}-{_uuid.uuid4().hex[:6].upper()}"
    new_env._state = create_initial_state(
        task_id=task_id,
        task_name=task.name,
        case_id=case_id,
        facts=modified_facts,
        max_steps=task.max_steps,
    )
    new_env._task_gold = task.gold_standard
    new_env._rewards_log = []

    _sessions[new_session_id] = new_env

    from environment.state import state_to_observation
    obs = state_to_observation(new_env._state, last_result="What-If episode started with modified facts.")

    return {
        "new_session_id": new_session_id,
        "original_session_id": req.session_id,
        "modified_fact": req.modified_fact,
        "observation": obs.model_dump(),
    }


# ---------------------------------------------------------------------------
# Case Memory
# ---------------------------------------------------------------------------

_case_memory: List[Dict[str, Any]] = []


@app.post("/api/memory/save")
async def save_case(session_id: str):
    """Save completed case to memory."""
    env = _sessions.get(session_id)
    if env is None:
        raise HTTPException(status_code=404, detail="Session not found.")
    ep = env.episode_result()
    if ep is None:
        raise HTTPException(status_code=400, detail="Episode not complete.")
    state = env.state()
    memory_entry = {
        "session_id": session_id,
        "case_id": state.get("case_id"),
        "task_id": state.get("task_id"),
        "task_name": state.get("task_name"),
        "final_score": ep.final_score,
        "total_steps": ep.total_steps,
        "final_analysis": ep.final_analysis,
        "legal_domain": state.get("legal_domain"),
        "identified_laws": [l["reference"] for l in state.get("identified_laws", [])],
        "recommended_actions": state.get("recommended_actions", []),
        "action_history": state.get("action_history", []),
        "completed_at": state.get("completed_at"),
    }
    _case_memory.append(memory_entry)
    return {"saved": True, "memory_count": len(_case_memory)}


@app.get("/api/memory")
async def get_memory():
    """Retrieve all saved case memories."""
    return {"cases": _case_memory, "count": len(_case_memory)}


# ---------------------------------------------------------------------------
# Serve frontend (production)
# ---------------------------------------------------------------------------

_frontend_dist = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend", "dist")

if os.path.exists(_frontend_dist):
    app.mount("/assets", StaticFiles(directory=os.path.join(_frontend_dist, "assets")), name="assets")

    @app.get("/{full_path:path}", include_in_schema=False)
    async def serve_spa(full_path: str):
        index_path = os.path.join(_frontend_dist, "index.html")
        if os.path.exists(index_path):
            return FileResponse(index_path)
        return JSONResponse({"message": "LegalLens 2.0 API — frontend not built yet"})
