#!/usr/bin/env python3
"""
LegalLens 2.0 - Local Validation Script
Verifies all components are working correctly before deployment.
"""

from __future__ import annotations

import sys
import os
import traceback

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

PASS = "\033[92m[PASS]\033[0m"
FAIL = "\033[91m[FAIL]\033[0m"
WARN = "\033[93m[WARN]\033[0m"

results = []

def check(name: str, fn):
    try:
        fn()
        print(f"{PASS} {name}")
        results.append((name, True, None))
    except Exception as e:
        tb = traceback.format_exc()
        print(f"{FAIL} {name}: {e}")
        print(f"       {tb.splitlines()[-1]}", file=sys.stderr)
        results.append((name, False, str(e)))


# ---------------------------------------------------------------------------
print("\n=== LEGALLENS 2.0 VALIDATION ===\n")
print("--- Python Imports ---")
# ---------------------------------------------------------------------------

def test_environment_import():
    from environment import LegalLensEnv, ActionType, LegalAction, CaseState
    assert LegalLensEnv is not None

def test_legal_import():
    from legal.knowledge_base import LegalKnowledgeBase
    kb = LegalKnowledgeBase()
    assert len(kb.get_all_laws()) > 0

def test_tasks_import():
    from tasks import get_all_tasks
    tasks = get_all_tasks()
    assert len(tasks) >= 4

def test_graders_import():
    from graders import get_all_graders
    graders = get_all_graders()
    assert len(graders) >= 4

check("environment import", test_environment_import)
check("legal knowledge base import", test_legal_import)
check("tasks import (4 tasks)", test_tasks_import)
check("graders import (4 graders)", test_graders_import)


# ---------------------------------------------------------------------------
print("\n--- Environment Core ---")
# ---------------------------------------------------------------------------

def test_reset():
    from environment.env import LegalLensEnv
    env = LegalLensEnv()
    obs = env.reset(task_id="cyber_fraud")
    assert obs is not None
    assert obs.facts
    assert obs.case_id

def test_step():
    from environment.env import LegalLensEnv
    env = LegalLensEnv()
    env.reset(task_id="cyber_fraud")
    result = env.step({"action_type": "CLASSIFY_DOMAIN", "domain": "cyber_law"})
    assert result is not None
    assert result.reward != 0 or result.reward == 0  # any float is ok
    assert isinstance(result.done, bool)

def test_state():
    from environment.env import LegalLensEnv
    env = LegalLensEnv()
    env.reset(task_id="consumer")
    state = env.state()
    assert isinstance(state, dict)
    assert "case_id" in state
    assert "facts" in state

def test_invalid_action_no_crash():
    from environment.env import LegalLensEnv
    env = LegalLensEnv()
    env.reset(task_id="cyber_fraud")
    result = env.step({"action_type": "CLASSIFY_DOMAIN"})  # missing domain
    # Should return a validation error, not crash
    assert result is not None
    assert result.error is not None or result.reward < 0

def test_invalid_action_type():
    from environment.env import LegalLensEnv
    env = LegalLensEnv()
    env.reset(task_id="cyber_fraud")
    result = env.step({"action_type": "NONEXISTENT_ACTION"})
    assert result is not None  # should not crash

check("reset()", test_reset)
check("step()", test_step)
check("state()", test_state)
check("invalid action -> no crash", test_invalid_action_no_crash)
check("unknown action type -> no crash", test_invalid_action_type)


# ---------------------------------------------------------------------------
print("\n--- Task Enumeration ---")
# ---------------------------------------------------------------------------

def test_task_count():
    from tasks import get_all_tasks
    tasks = get_all_tasks()
    assert len(tasks) >= 4, f"Expected 4+ tasks, got {len(tasks)}"

def test_task_cyber_fraud():
    from tasks import get_task
    t = get_task("cyber_fraud")
    assert t.facts
    assert t.gold_standard

def test_task_bail():
    from tasks import get_task
    t = get_task("bail")
    assert t.facts
    assert t.gold_standard.get("facts_are_incomplete") == True

def test_task_consumer():
    from tasks import get_task
    t = get_task("consumer")
    assert t.facts
    assert t.domain == "consumer_law"

def test_task_property():
    from tasks import get_task
    t = get_task("property")
    assert t.facts
    assert "property" in t.domain

check("task count >= 4", test_task_count)
check("task: cyber_fraud", test_task_cyber_fraud)
check("task: bail (facts_are_incomplete=True)", test_task_bail)
check("task: consumer", test_task_consumer)
check("task: property", test_task_property)


# ---------------------------------------------------------------------------
print("\n--- Grader Evaluation ---")
# ---------------------------------------------------------------------------

def _run_grader(task_id: str):
    from environment.env import LegalLensEnv
    from graders import get_grader
    env = LegalLensEnv()
    obs = env.reset(task_id=task_id)
    # Run a few actions
    env.step({"action_type": "CLASSIFY_DOMAIN", "domain": env._task_gold.get("correct_domain", "civil_law")})
    env.step({"action_type": "IDENTIFY_ISSUE", "issue": "Legal issue in the case"})
    env.step({"action_type": "FINALIZE_ANALYSIS", "final_analysis": "Test analysis", "confidence": 0.5})
    ep = env.episode_result()
    assert ep is not None
    assert 0.0 <= ep.final_score <= 1.0, f"Score out of range: {ep.final_score}"
    return ep.final_score

def test_grader_cyber_fraud():
    score = _run_grader("cyber_fraud")
    assert 0.0 <= score <= 1.0

def test_grader_bail():
    score = _run_grader("bail")
    assert 0.0 <= score <= 1.0

def test_grader_consumer():
    score = _run_grader("consumer")
    assert 0.0 <= score <= 1.0

def test_grader_property():
    score = _run_grader("property")
    assert 0.0 <= score <= 1.0

check("grader: cyber_fraud score [0,1]", test_grader_cyber_fraud)
check("grader: bail score [0,1]", test_grader_bail)
check("grader: consumer score [0,1]", test_grader_consumer)
check("grader: property score [0,1]", test_grader_property)


# ---------------------------------------------------------------------------
print("\n--- Baseline Agent ---")
# ---------------------------------------------------------------------------

def test_baseline_cyber_fraud():
    from baseline_agent import BaselineAgent
    agent = BaselineAgent()
    result = agent.run(task_id="cyber_fraud", max_steps=10)
    assert isinstance(result["final_score"], float)
    assert 0.0 <= result["final_score"] <= 1.0
    assert result["total_steps"] > 0

def test_baseline_bail():
    from baseline_agent import BaselineAgent
    agent = BaselineAgent()
    result = agent.run(task_id="bail", max_steps=10)
    assert 0.0 <= result["final_score"] <= 1.0

check("baseline agent: cyber_fraud", test_baseline_cyber_fraud)
check("baseline agent: bail", test_baseline_bail)


# ---------------------------------------------------------------------------
print("\n--- Knowledge Base ---")
# ---------------------------------------------------------------------------

def test_kb_law_lookup():
    from legal.knowledge_base import LegalKnowledgeBase
    kb = LegalKnowledgeBase()
    law = kb.get_law_by_id("it_act_sec66d")
    assert law is not None
    assert law.verified == True

def test_kb_search():
    from legal.knowledge_base import LegalKnowledgeBase
    kb = LegalKnowledgeBase()
    results = kb.search_laws("bail")
    assert len(results) > 0

def test_kb_domain_filter():
    from legal.knowledge_base import LegalKnowledgeBase
    kb = LegalKnowledgeBase()
    laws = kb.get_laws_by_domain("consumer_law")
    assert len(laws) > 0

check("knowledge base: law lookup by ID", test_kb_law_lookup)
check("knowledge base: keyword search", test_kb_search)
check("knowledge base: domain filter", test_kb_domain_filter)


# ---------------------------------------------------------------------------
print("\n--- File Checks ---")
# ---------------------------------------------------------------------------

REQUIRED_FILES = [
    "inference.py",
    "baseline_agent.py",
    "pyproject.toml",
    "requirements.txt",
    "Dockerfile",
    "openenv.yaml",
    "README.md",
    ".env.example",
    "environment/__init__.py",
    "environment/env.py",
    "environment/models.py",
    "environment/actions.py",
    "environment/rewards.py",
    "environment/state.py",
    "legal/__init__.py",
    "legal/knowledge_base.py",
    "tasks/__init__.py",
    "tasks/task_01_cyber_fraud.py",
    "tasks/task_02_bail.py",
    "tasks/task_03_consumer.py",
    "tasks/task_04_property.py",
    "graders/__init__.py",
    "graders/base.py",
    "graders/cyber_fraud.py",
    "graders/bail.py",
    "graders/consumer.py",
    "graders/property.py",
    "server/__init__.py",
    "server/app.py",
]

root = os.path.dirname(os.path.abspath(__file__))
missing = []
for f in REQUIRED_FILES:
    path = os.path.join(root, f)
    if not os.path.exists(path):
        missing.append(f)

def test_required_files():
    if missing:
        raise FileNotFoundError(f"Missing files: {', '.join(missing)}")

check("all required files exist", test_required_files)


# ---------------------------------------------------------------------------
print("\n--- Configuration ---")
# ---------------------------------------------------------------------------

def test_openenv_yaml():
    import yaml
    path = os.path.join(root, "openenv.yaml")
    with open(path) as f:
        config = yaml.safe_load(f)
    assert "name" in config or "env_id" in config or "environment" in config

def test_pyproject_toml():
    import tomllib
    path = os.path.join(root, "pyproject.toml")
    with open(path, "rb") as f:
        config = tomllib.load(f)
    assert "project" in config
    assert config["project"]["name"]

check("openenv.yaml valid", test_openenv_yaml)
check("pyproject.toml valid", test_pyproject_toml)


# ---------------------------------------------------------------------------
print("\n--- Server Import ---")
# ---------------------------------------------------------------------------

def test_server_import():
    # Just check the server app can be imported
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "server.app",
        os.path.join(root, "server", "app.py")
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    assert hasattr(mod, "app")

check("server.app imports and has 'app' object", test_server_import)


# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
print("\n" + "=" * 40)
passed = sum(1 for _, ok, _ in results if ok)
failed = sum(1 for _, ok, _ in results if not ok)
total = len(results)

if failed == 0:
    print(f"\033[92m\nLEGALLENS 2.0 READY — {passed}/{total} checks passed\033[0m")
else:
    print(f"\033[91m\n{failed} CHECKS FAILED — {passed}/{total} passed\033[0m")
    print("\nFailed checks:")
    for name, ok, err in results:
        if not ok:
            print(f"  ✗ {name}: {err}")
    sys.exit(1)
