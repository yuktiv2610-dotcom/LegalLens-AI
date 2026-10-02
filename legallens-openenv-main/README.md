# LegalLens 2.0

**LegalLens 2.0** is an OpenEnv AI legal reasoning environment and interactive simulation platform focused on Indian Law.

## Overview

LegalLens provides a structured legal investigation environment where an AI agent can:
- Be presented with a complex factual scenario
- Investigate through a structured action space (`CLASSIFY_DOMAIN`, `IDENTIFY_ISSUE`, `IDENTIFY_LAW`, `REQUEST_EVIDENCE`, etc.)
- Receive step-by-step observations, feedback, and rewards
- Earn a normalized evaluation score (0.0 - 1.0) based on legal accuracy and completeness.

## Features
- **Genuine OpenEnv Compliance**: Exposes standard `reset()`, `step()`, and `state()` methods.
- **4 Benchmark Tasks**: Cyber Fraud, Criminal Bail, Consumer Dispute, and Property Title.
- **Robust Reward Engine**: Rewards correct steps and penalizes hallucinations/fabricated laws.
- **Uncertainty Recognition**: The Bail and Property tasks intentionally omit critical facts. The agent earns extra credit for correctly identifying and querying `INSUFFICIENT INFORMATION`.
- **Pixel-Art Frontend**: A complete React + Vite UI showcasing the investigation process live.

## Quickstart

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Run the baseline agent locally:**
   ```bash
   python baseline_agent.py
   ```
3. **Run validation tests:**
   ```bash
   python validate_local.py
   ```
4. **Start the API server (and frontend if built):**
   ```bash
   uvicorn server.app:app --host 0.0.0.0 --port 7860
   ```

## Repository Structure
- `/environment/`: Core `LegalLensEnv`, State management, Actions, and Rewards.
- `/legal/`: Verified Indian legal knowledge base (laws, regulations).
- `/tasks/`: Benchmark legal task definitions.
- `/graders/`: Specialized grading logic for each task type.
- `/server/`: FastAPI endpoints.
- `/frontend/`: Pixel-art React UI (run `npm run build` to compile into `/dist`).

## Inference / LLM Evaluation
Run the included OpenEnv-compatible LLM inference script:
```bash
export API_BASE_URL=https://api.openai.com/v1
export MODEL_NAME=gpt-4o-mini
export HF_TOKEN=sk-your-token
python inference.py cyber_fraud
```

## Disclaimer
LegalLens is an AI-assisted informational tool. It does not provide professional legal advice.
